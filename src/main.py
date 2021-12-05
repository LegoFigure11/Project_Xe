from xoroshiro import XOROSHIRO
from calc import motions2seed

motions = []
print("128 Inputs (Click stick on summary screen - 0: Physical/1: Special):")
for n in range(128):
    motions.append(int(input(":")))
    print(f"{n+1:03d}/128 (0 Phys/1 Spec)")
seed = motions2seed(motions)
initial_advances = 128
print(f"Seed {seed:016X} Initial Advance {initial_advances}")
print(f"S[0]: {(seed >> 64):016X}")
print(f"S[1]: {(seed & 0xFFFFFFFFFFFFFFFF):016X}")