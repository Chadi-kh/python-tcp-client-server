import os
import sys
import socket

if len(sys.argv) < 3:
    print("Usage: python3 server_mem.py <memsize> <port> [--debug] [--periodic-log logfile]")
    sys.exit(1)

try:
    memsize = int(sys.argv[1])
    port = int(sys.argv[2])
except ValueError:
    print("error: memsize and port must be integers")
    sys.exit(1)

debug = False
periodic_log = False
logfile = None

if len(sys.argv) == 3:
    pass
elif len(sys.argv) == 4 and sys.argv[3] == "--debug":
    debug = True
elif len(sys.argv) == 5 and sys.argv[3] == "--periodic-log":
    periodic_log = True
    logfile = sys.argv[4]
elif len(sys.argv) == 6 and sys.argv[3] == "--debug" and sys.argv[4] == "--periodic-log":
    debug = True
    periodic_log = True
    logfile = sys.argv[5]
else:
    print("error: invalid arguments")
    sys.exit(1)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", port))
server_socket.listen(5)

# pipe parent -> frontend
p_to_f_read, p_to_f_write = os.pipe()
# pipe frontend -> backend
f_to_b_read, f_to_b_write = os.pipe()
# pipe backend -> parent
b_to_p_read, b_to_p_write = os.pipe()
# pipe erreur frontend -> parent
f_err_read, f_err_write = os.pipe()

pid_front = os.fork()

if pid_front == 0:
    # frontend lit depuis le parent
    os.dup2(p_to_f_read, 0)

    # frontend écrit vers backend
    os.dup2(f_to_b_write, 1)

    # erreurs frontend vers parent
    os.dup2(f_err_write, 2)
    args = ["python3", "server_mem_frontend.py", str(memsize)]
    if debug:
        args.append("--debug")

    os.execvp("python3", args)

pid_back = os.fork()

if pid_back == 0:
    # backend lit depuis frontend
    os.dup2(f_to_b_read, 0)

    # backend écrit vers parent
    os.dup2(b_to_p_write, 1)
    args = ["python3", "server_mem_backend.py", str(memsize)]

    if periodic_log:
        logfd = os.open(logfile, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
        os.dup2(logfd, 2)
        os.close(logfd)
        args.append("--periodic-log")

    os.execvp("python3", args)

# le parent ferme les bouts inutiles
os.close(p_to_f_read)
os.close(f_to_b_read)
os.close(f_to_b_write)
os.close(b_to_p_write)
os.close(f_err_write)


while True:
    socket_client, adresse_client = server_socket.accept()
    data = socket_client.recv(1024)

    if not data:
        socket_client.close()
        continue

    if not data.endswith(b"\n"):
        data += b"\n"

    # envoyer la commande au frontend
    os.write(p_to_f_write, data)

    instruction = data.decode().split()[0]

    # PUT / DELETE répondent depuis le frontend
    if instruction == "PUT" or instruction == "DELETE":
        reponse = os.read(f_err_read, 1024)

    # GET / POST répondent normalement depuis le backend
    else:
        reponse = os.read(b_to_p_read, 1024)


    socket_client.sendall(reponse)
    socket_client.close()
os.wait()
os.wait()