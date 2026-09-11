import os
import sys
import signal

def log_memory(signum, frame):
    print(list(memory), file=sys.stderr)
    signal.alarm(1)

if len(sys.argv) < 2:
    print("Usage: python3 server_mem_backend.py memsize [--periodic-log]", flush=True)
    sys.exit(1)

taille = int(sys.argv[1])
memory = bytearray([32] * taille)

periodic = False
if len(sys.argv) == 3 and sys.argv[2] == "--periodic-log":
    periodic = True

if periodic:
    signal.signal(signal.SIGALRM, log_memory)
    signal.alarm(1)

for ligne in sys.stdin:
    ligne = ligne.strip()

    if ligne == "":
        continue

    partie = ligne.split()
    instruction = partie[0]

    if instruction == "GET":
        if len(partie) != 2:
            print("error", flush=True)
            continue

        try:
            i = int(partie[1])
        except ValueError:
            print("error", flush=True)
            continue

        if i < 0 or i >= taille:
            print(f"error: index {i} out of bounds", flush=True)
        else:
            print(memory[i], flush=True)

    elif instruction == "POST":
        if len(partie) != 3:
            print("error", flush=True)
            continue

        try:
            i = int(partie[1])
            valeur = int(partie[2])
        except ValueError:
            print("error", flush=True)
            continue

        if i < 0 or i >= taille:
            print(f"error: index {i} out of bounds", flush=True)
        elif valeur < 0 or valeur > 255:
            print(f'error: POST instruction requires a byte as a second argument "{valeur}" out of byte range (0-255)', flush=True)
        else:
            memory[i] = valeur
            print("ok", flush=True)

    else:
        print("error", flush=True)

print("bye", flush=True)