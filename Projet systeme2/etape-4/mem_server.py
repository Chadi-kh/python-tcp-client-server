import os
import sys

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

fd_read, fd_write = os.pipe()

pid_front = os.fork()

if pid_front == 0:
    os.dup2(fd_write, 1)

    os.close(fd_read)
    os.close(fd_write)

    args = ["python3", "server_mem_frontend.py", str(memsize)]
    if debug:
        args.append("--debug")

    os.execvp("python3", args)

pid_back = os.fork()

if pid_back == 0:
    os.dup2(fd_read, 0)

    os.close(fd_read)
    os.close(fd_write)

    args = ["python3", "server_mem_backend.py", str(memsize)]

    if periodic_log:
        logfd = os.open(logfile, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
        os.dup2(logfd, 2)
        os.close(logfd)
        args.append("--periodic-log")

    os.execvp("python3", args)

os.close(fd_read)
os.close(fd_write)

os.wait()
os.wait()