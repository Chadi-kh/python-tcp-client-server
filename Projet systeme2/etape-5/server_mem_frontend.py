import sys

if len(sys.argv) < 2:
    print("Usage: python3 server_mem_frontend.py memsize [--debug]", flush=True)
    sys.exit(1)

taille = int(sys.argv[1])

debug = False
if len(sys.argv) == 3 and sys.argv[2] == "--debug":
    debug = True

segments_table = {}

def print_debug():
    if debug:
        print(f"[debug] segments_table={segments_table}", file=sys.stderr, flush=True)

for ligne in sys.stdin:
    ligne = ligne.strip()
    if ligne == "":
        continue

    partie = ligne.split()
    instruction = partie[0]

    if instruction == "GET":
        if len(partie) != 3:
            print("error", file=sys.stderr, flush=True)
            continue

        segname = partie[1]

        try:
            indice = int(partie[2])
        except ValueError:
            print("error", file=sys.stderr, flush=True)
            continue

        if segname not in segments_table:
            print(f"error: unknown segment {segname}", file=sys.stderr, flush=True)
            continue

        base = segments_table[segname]["base"]
        size = segments_table[segname]["size"]

        if indice < 0 or indice >= size:
            print(f"error: index {indice} out of bounds, {segname} size is {size}", file=sys.stderr, flush=True)
            continue

        adresse = base + indice
        print(f"GET {adresse}", flush=True)

    elif instruction == "PUT":
        if len(partie) != 3:
            print("error", file=sys.stderr, flush=True)
            continue

        segname = partie[1]

        try:
            size = int(partie[2])
        except ValueError:
            print("error", file=sys.stderr, flush=True)
            continue

        if segname in segments_table:
            print(f"error: segment {segname} already exists", file=sys.stderr, flush=True)
            continue

        if size <= 0 or size > taille:
            print(f"error: invalid size {size}", file=sys.stderr, flush=True)
            continue

        candidats = [0]
        for seg in segments_table.values():
            candidats.append(seg["base"] + seg["size"])

        placed = False

        for a in candidats:
            if a + size > taille:
                continue

            new_start = a
            new_end = a + size - 1
            overlap = False

            for seg in segments_table.values():
                old_start = seg["base"]
                old_end = old_start + seg["size"] - 1

                if not (new_end < old_start or new_start > old_end):
                    overlap = True
                    break

            if not overlap:
                segments_table[segname] = {"base": a, "size": size}
                print_debug()
                print("ok", file=sys.stderr, flush=True)
                placed = True
                break

        if not placed:
            print(f"error: not enough memory to create segment {segname} of size {size}", file=sys.stderr, flush=True)

    elif instruction == "POST":
        if len(partie) != 4:
            print("error", file=sys.stderr, flush=True)
            continue

        segname = partie[1]

        try:
            indice = int(partie[2])
            valeur = int(partie[3])
        except ValueError:
            print("error", file=sys.stderr, flush=True)
            continue

        if segname not in segments_table:
            print(f"error: unknown segment {segname}", file=sys.stderr, flush=True)
            continue

        base = segments_table[segname]["base"]
        size = segments_table[segname]["size"]

        if indice < 0 or indice >= size:
            print(f"error: index {indice} out of bounds, {segname} size is {size}", file=sys.stderr, flush=True)
            continue

        if valeur < 0 or valeur > 255:
            print(f'error: POST instruction requires a byte as a second argument "{valeur}" out of byte range (0-255)', file=sys.stderr, flush=True)
            continue

        adresse = base + indice
        print(f"POST {adresse} {valeur}", flush=True)

    elif instruction == "DELETE":
        if len(partie) != 2:
            print("error", file=sys.stderr, flush=True)
            continue

        segname = partie[1]

        if segname not in segments_table:
            print(f"error: unknown segment {segname}", file=sys.stderr, flush=True)
            continue

        del segments_table[segname]
        print_debug()
        print("ok", file=sys.stderr, flush=True)

    else:
        print("error", file=sys.stderr, flush=True)