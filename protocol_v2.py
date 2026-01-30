import schnorr
import time

from crypto import rand_int, hash_to_int, hashmac_to_str
from zipcode import inset, outset


def protocol_v2(delta, T, alpha, y, group):
    n = len(T)
    p,q,g = group

    # print("Alice register to the Accorderie")
    delta_ = hashmac_to_str(delta, alpha)

    # print("Bob send T to the Accorderie")
    _st = time.time()
    sr_set = [schnorr.sign(hashmac_to_str(t, alpha), x, group) for t in T]
    # print("The Accorderie send {s,r} to Bob")

    s, r = zip(*sr_set)
    # print("Bob publish {s,r} ")
    pub_time = time.time() - _st

    _st = time.time()
    for i in range(n):
        if (S:=r[i] * pow(y, hash_to_int(str(r[i]) + delta_), p) % p) == pow(g, s[i], p):
            # print("Alice find a match")
            # print("Alice send S to Bob")

            for s,r in sr_set:
                if S == pow(g,s,p):
                    # print(f"Bob confirm")
                    break
            else:
                raise
            break
    else:
        # print(f"Alice find no match")
        pass
    # print(f"{i=}")
    verify_time = time.time() - _st

    return pub_time, verify_time


if __name__ == "__main__":
    group = schnorr.load_group(0)
    x, y = schnorr.gen_keys(group)
    alpha = rand_int()

    stat = dict()
    n = 100
    for set_size in [100, 200, 300, 400, 500]:
        print(f"{set_size=}")
        times = []
        for i in range(n):
            print(f"\r    {i:>3}/{n}", end="")
            alice_address, bob_set = inset(set_size)
            times.append(protocol_v2(alice_address, bob_set, alpha, y, group))

        print("\r    Done")
        times = zip(*times)
        stat[set_size] = [round(sum(t) / n * 1000) for t in times]

    print(f"v2 = {stat}")

# inset
# {32: [67, 108], 64: [131, 201], 128: [261, 397], 256: [519, 777], 512: [1039, 1490], 1024: [2066, 2981]}
# {100: [198, 303], 200: [394, 575], 300: [593, 897], 400: [794, 1139], 500: [990, 1394]}
