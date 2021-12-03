from xoroshiro import XOROSHIRO
from generator import Filter, OverworldRNG
from calc import motions2seed

ms = int(input("Motions or seed? (0/1): "))
if ms == 0:
    motions = []
    print("128 pokemon motions (0:phy/1:spc):")
    for n in range(128):
        motions.append(int(input(":")))
        print(f"{n+1:03d}/128")
    seed = motions2seed(motions)
    initial_advances = 128
    print(f"Seed {seed:08X} Initial Advance {initial_advances}")
else:
    seed = int(input("Seed: 0x"),16)
    initial_advances = int(input("Initial Advances: "))
    print(f"Seed {seed:08X} Initial Advance {initial_advances}")
filter = Filter(
    iv_min=None,
    iv_max=None,
    abilities=None,
    shininess="Star/Square",
    slot_min=None,
    slot_max=None,
    natures=None,
    marks=None
    )
generator = OverworldRNG(
    seed=seed,
    tid=61257,
    sid=1240,
    shiny_charm=True,
    mark_charm=True,
    weather_active=True,
    is_fishing=False,
    is_static=True,
    is_legendary=False,
    is_shiny_locked=False,
    min_level=60,
    max_level=60,
    diff_held_item=False,
    filter=filter,
    double_mark_gen=False
    )
generator.advance_fast(initial_advances)

for _ in range(int(input("Max Advances: "))):
    state = generator.generate()
    if state:
        print(state)