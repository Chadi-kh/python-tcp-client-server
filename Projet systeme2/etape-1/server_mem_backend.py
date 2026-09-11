import sys

if len(sys.argv) != 2:
    print("Usage: server_mem_backend taille")
    sys.exit(1)

try:
    taille = int(sys.argv[1])
except ValueError:
    print("error: memsize must be an integer")
    sys.exit(1)

memory = bytearray([32] * taille)

for ligne in sys.stdin:
    ligne = ligne.strip()
    if ligne == "":
        continue

    partie = ligne.split()
    instruction = partie[0]

    if instruction == "GET":
        if len(partie) != 2:
            print("error")
            continue

        try:
            i = int(partie[1])
        except ValueError:
            print("error")
            continue

        if i < 0 or i >= taille:
            print(f"error: index {i} out of bounds")
        else:
            print(memory[i])

    elif instruction == "POST":
        if len(partie) != 3:
            print("error")
            continue

        try:
            i = int(partie[1])
            valeur = int(partie[2])
        except ValueError:
            print("error")
            continue

        if i < 0 or i >= taille:
            print(f"error: index {i} out of bounds")
        elif valeur < 0 or valeur > 255:
            print(f'error: POST instruction requires a byte as a second argument "{valeur}" out of byte range (0-255)')
        else:
            memory[i] = valeur
            print("ok")

    else:
        print("error")

print("bye")