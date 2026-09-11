import sys, random
from remotememory import RemoteMemory
from controledmemory import ControledMemory

# paramÃ¨tres (modifiables en ligne de commande)
write_rate = 0.1 # 10% d'Ã©critures
sigma = 3 # Ã©cart-type de la distribution normale
num_accesses = 1000 # nombre d'accÃ¨s Ã  la mÃ©moire
debug = False # afficher les messages de debug
alloc = True
# lecture des arguments de la ligne de commande
try:
    if "--write_rate" in sys.argv:
        write_rate = float(sys.argv[sys.argv.index("--write_rate") + 1])
    if "--sigma" in sys.argv:
        sigma = float(sys.argv[sys.argv.index("--sigma") + 1])
    if "--num_accesses" in sys.argv:
        num_accesses = int(sys.argv[sys.argv.index("--num_accesses") + 1])
    if "--debug" in sys.argv:
        debug = True
    if "--no-alloc" in sys.argv:
        alloc=False
    host = sys.argv[1]
    port = int(sys.argv[2])
    segname = sys.argv[3]
    segsize = int(sys.argv[4])
except:
    print("Usage: python client.py <host> <port> <segname> <segsize> OPTIONS\nOPTIONS:\n  --write_rate <float>  taux d'Ã©criture (dÃ©faut: 0.1)\n  --sigma <float>       Ã©cart-type de la distribution normale (dÃ©faut: 3)\n  --num_accesses <int>  nombre d'accÃ¨s Ã  la mÃ©moire (dÃ©faut: 1000)\n  --debug               afficher les messages de debug", file=sys.stderr)
    sys.exit(1)

index = 0

# crÃ©ation de la mÃ©moire contrÃ´lÃ©e
with ControledMemory(RemoteMemory(host, port, segname, segsize, debug,alloc)) as mem:
    # boucle de lecture/Ã©criture
    for i in range(num_accesses):
        index = int(random.gauss(index, sigma)) % segsize
        if random.random() < write_rate:
            mem[index] = random.randint(0, 255)            
        else:
            _ = mem[index]
