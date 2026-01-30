import schnorr
import time

from crypto import rand_int, hash_to_int, hashmac_to_str
from zipcode import inset, outset


def protocol_v3(delta, T, alpha, y, group):
    n = len(T)
    p,q,g = group

    # print("Alice register to the Accorderie")
    delta_ = hashmac_to_str(delta, alpha)

    # print("Bob send T to the Accorderie")

    _st = time.time()
    sr_set = [schnorr.sign(hashmac_to_str(t, alpha), x, group) for t in T]
    z = rand_int()
    y_ = pow(y, z, p)
    S_ = [pow(g, s*z%q, p) for s,r in sr_set]
    r_ = [pow(r,z,p) for s,r in sr_set]
    r = [r for s,r in sr_set]
    # print("The Accorderie publish y',{S',r',r}")
    # print("The Accorderie send z to Bob")
    pub_time = time.time() - _st

    _st = time.time()
    for i in range(n):
        if r_[i] * pow(y_, hash_to_int(str(r[i]) + delta_), p) % p == S_[i]:
            # print("Alice find a match")
            S = r[i] * pow(y, hash_to_int(str(r[i]) + delta_), p) % p
            # print("Alice send S to Bob")

            verif = pow(S,z,p) in S_
            assert verif
            # print(f"Bob confirm: {verif}")
            break
    else:
        # print(f"Alice find no match")
        pass
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
            times.append(protocol_v3(alice_address, bob_set, alpha, y, group))

        print("\r    Done")
        times = zip(*times)
        stat[set_size] = [round(sum(t) / n * 1000) for t in times]

    print(f"v3 = {stat}")

# inset
# {32: [192, 37], 64: [384, 67], 128: [768, 148], 256: [1541, 269], 512: [3102, 499], 1024: [6216, 952]}
# {100: [594, 99], 200: [1181, 203], 300: [1788, 317], 400: [2366, 391], 500: [2949, 503]}
#
# outset
# {32: [191, 63], 64: [381, 127], 128: [777, 259], 256: [1543, 511], 512: [3064, 1019], 1024: [6003, 2007]}
