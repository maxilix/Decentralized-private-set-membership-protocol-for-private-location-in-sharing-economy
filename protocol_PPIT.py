import schnorr
from crypto import rand_int, hash_to_int, hash_to_bytes, aes_encrypt, aes_decrypt


def protocol_PPIT(client_id_sign, server_id, server_entry, y, group):
    p,q,g = group
    
    r = client_id_sign[1]
    # print("Client send r to Server")

    z = rand_int()
    Z = pow(g, z, p)
    ks = hash_to_bytes(str(pow(r * pow(y, hash_to_int(str(r)+server_id), p) % p, z, p)).encode())[:16]
    D = aes_encrypt(server_entry, ks)

    # print("Server send D and Z to Client")

    kc = hash_to_bytes(str(pow(Z, client_id_sign[0], p)).encode())[:16]
    assert kc == ks
    d = aes_decrypt(D, kc)
    assert d == server_entry

    # print(f"Client retrieve server entry: {d}")


if __name__ == "__main__":
    group = schnorr.load_group(0)
    x, y = schnorr.gen_keys(group)

    client_id = "foobar"
    client_id_sign = schnorr.sign(client_id, x, group)

    server_id = "foobar"
    server_entry = "awesome entry"

    protocol_PPIT(client_id_sign, server_id, server_entry, y, group)
