from xoroshiro import XOROSHIRO
import calc

def main():
    prng = XOROSHIRO(0x123456789ABCDEF,0xFEDCBA9876543210)

    s0, s1 = prng.seed
    print(f"expected: s0 {s0:016X} s1 {s1:016X}")
    
    observed = [prng.next()%2 for _ in range(128)]
    s0, s1 = calc.motions2state(observed)

    print(f"result: s0 {s0:016X} s1 {s1:016X}")

if __name__ == "__main__":
    main()
    