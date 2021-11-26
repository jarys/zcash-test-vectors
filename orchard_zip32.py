#!/usr/bin/env python3

from utils import i2leosp
from pyblake2 import blake2b
from sapling_key_components import prf_expand

class ExtendedSpendingKey:
    def __init__(self, sk, c):
        self.sk = sk
        self.c = c

    @staticmethod
    def master(secret):
        I = blake2b(person=b'ZcashIP32Orchard', data=secret).digest()
        return ExtendedSpendingKey(sk=I[:32],c=I[32:])

    def child(self, i):
        assert i >= 1<<31
        I = prf_expand(self.c, bytes([0x81]) + self.sk + i2leosp(32, i))
        return ExtendedSpendingKey(sk=I[:32],c=I[32:])

    def derive(self, path):
        state = self
        for digit in path:
            state = state.child(digit)
        return state.sk

if __name__ == "__main__":

    from random import Random
    from tv_rand import Rand

    rng = Random(0xabad533d)
    def randbytes(l):
        ret = []
        while len(ret) < l:
            ret.append(rng.randrange(0, 256))
        return bytes(ret)
    rand = Rand(randbytes)

    H = 1 << 31
    paths = [
        [32|H, 133|H, 0|H],
        [32|H, 133|H, 5|H],
        [32|H, 133|H, 99|H],
        [32|H, 1|H, 0|H],
        [32|H, 1|H, 3|H]
    ]

    test_vectors = []
    for path in paths:
        seed = rand.b(32)
        sk = ExtendedSpendingKey.master(seed).derive(path)
        test_vectors.append({
            "seed": seed,
            "path": path,
            "sk": sk
        })

    print("TESTVECTORS_ZIP32 = [")
    for tv in test_vectors:
        print("\t{")
        for key, value in tv.items():
            if key == "path":
                print(f"\t\t\"{key}\": {value},", end="")
                print(" # m/{}'/{}'/{}'".format(*map(lambda x: x^H, value)))
            else:
                print(f"\t\t\"{key}\": unhexlify(\"{value.hex()}\"),")
        print("\t},")
    print("]")

