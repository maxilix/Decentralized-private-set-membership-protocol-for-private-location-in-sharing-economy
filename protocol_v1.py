import schnorr
import time

from crypto import rand_int, hash_to_int, hash_to_str
from zipcode import inset, outset


def protocol_v1(delta, T, y, group):
    p,q,g = group

    _st = time.time()
    # print("Bob send T to the Accorderie")
    sr_set = [schnorr.sign(t, x, group) for t in T]
    # print("The Accorderie send {s,r} to Bob")

    zb = rand_int()
    B = [pow(g, (zb*s)%q, p) for s,r in sr_set]
    R = [r for s,r in sr_set]
    # print("Bob publish {b} and {r}")
    pub_time = time.time() - _st

    _st = time.time()

    za = rand_int()
    A = [pow(r * pow(y, hash_to_int(str(r) + delta), p) % p, za, p) for r in R]
    B_alice = [hash_to_str(pow(b, za, p)) for b in B]
    # print("Alice send {a} to Bob")

    A_ = [hash_to_str(pow(a, zb, p)) for a in A]
    # print("Bob send {a'} to Alice")

    if (m:=len(set(A_) & set(B_alice))) > 0:
        # print(f"Alice find {m} match")
        Za = pow(g, za, p)
        # print("Alice send Za to Bob")

        B_bob = [hash_to_str(pow(Za, (zb*s)%q, p)) for s,_ in sr_set]
        assert len(set(A_) & set(B_bob)) > 0
        # print(f"Bob confirm {len(set(A_) & set(B_bob))} match")
    else:
        # print(f"Alice find no match")
        pass

    verif_time = time.time() - _st

    return pub_time, verif_time


if __name__ == "__main__":
    group = schnorr.load_group(0)
    x, y = schnorr.gen_keys(group)

    stat = dict()
    n = 100
    for set_size in [100, 200, 300, 400, 500]:
        print(f"{set_size=}")
        times = []
        for i in range(n):
            print(f"\r    {i:>3}/{n}", end="")
            alice_address, bob_set = inset(set_size)
            times.append(protocol_v1(alice_address, bob_set, y, group))

        print("\r    Done")
        times = zip(*times)
        stat[set_size] = [round(sum(t) / n * 1000) for t in times]

    print(f"v1 = {stat}")

# inset
# {32: [128, 324], 64: [257, 647], 128: [508, 1274], 256: [1023, 2565], 512: [2005, 5025], 1024: [3977, 9959]}
# {100: [378, 948], 200: [757, 1901], 300: [1142, 2865], 400: [1527, 3829], 500: [1908, 4782]}
