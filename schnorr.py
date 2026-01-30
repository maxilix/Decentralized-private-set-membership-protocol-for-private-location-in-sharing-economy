import pickle
import random
import subprocess

from crypto import rand_int, hash_to_int

P_size=2048
# Q_size must be set to 256, as its value depends on the hashing function (hard-coded)

def _is_prime(p):
    r = subprocess.run(f"openssl prime {p}", shell=True, stdout=subprocess.PIPE)
    return "is prime" in r.stdout.decode("UTF-8")

def _gen_random(size):
    return random.randrange(2 ** (size - 1), 2 ** size)

def _gen_prime(size):
    rop = _gen_random(size)
    while not _is_prime(rop):
        rop = _gen_random(size)
    return rop

def sign(message, x, group):
    p,q,g = group
    k = rand_int()
    r = pow(g, k, p)
    s = (k + x * hash_to_int(str(r) + message)) % q
    return s, r

def verify(message, signature, y, group):
    p,q,g = group
    s, r = signature
    gs = pow(g, s, p)
    ryh = (r * pow(y, hash_to_int(str(r) + message), p)) % p
    return gs == ryh

def gen_group():
    """
    create a random Schnorr group
    https://en.wikipedia.org/wiki/Schnorr_group
    g is a generator of a subgroup of Zp* of order q
    where : p = q*r + 1
            h random in Zp
            g = h**r % p
    """
    p = 1
    q = _gen_prime(256)
    r = 1

    while not _is_prime(p):
        r = _gen_random(P_size - 256)
        p = q * r + 1

    g = 1
    while g == 1:
        h = random.randrange(2, p)
        g = pow(h, r, p)

    return p,q,g

def save_group(group, id):
    file = open(f"schnorr_group_{id}.data", 'wb')
    pickle.dump(group, file)
    file.close()

def load_group(id):
    file = open(f"schnorr_group_{id}.data", 'rb')
    group = pickle.load(file)
    file.close()
    return group

def gen_keys(group):
    p, q, g = group
    x = rand_int()
    y = pow(g, x, p)
    return x, y


if __name__ == "__main__":
    id = 0
    group = gen_group()
    save_group(group, id)
    print("Done")
