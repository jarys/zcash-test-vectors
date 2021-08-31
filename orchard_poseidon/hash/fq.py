#!/usr/bin/env python3
import sys; assert sys.version_info[0] >= 3, "Python 3 required."
sys.path.append('../..')

from orchard_vesta import Fq
from orchard_poseidon.permute.fq import perm
from utils import leos2ip
from tv_output import render_args, render_tv
from tv_rand import Rand

# Initial capacity element
CAPACITY_ELEMENT = Fq(1 << 65)

def poseidon_hash(x, y):
    assert isinstance(x, Fq)
    assert isinstance(y, Fq)
    return perm([x, y, CAPACITY_ELEMENT])[0]

def main():
    test_vectors = [[Fq.ZERO, Fq(1)]]

    from random import Random
    rng = Random(0xabad533d)
    def randbytes(l):
        ret = []
        while len(ret) < l:
            ret.append(rng.randrange(0, 256))
        return bytes(ret)
    rand = Rand(randbytes)

    # Generate random test vectors
    for _ in range(10):
        test_vectors.append([
            Fq(leos2ip(rand.b(32))),
            Fq(leos2ip(rand.b(32))),
        ])

    render_tv(
        render_args(),
        'orchard_poseidon/hash/fq',
        (
            ('input', '[[u8; 32]; 2]'),
            ('output', '[u8; 32]'),
        ),
        [{
            'input': list(map(bytes, input)),
            'output': bytes(poseidon_hash(input[0], input[1])),
        } for input in test_vectors],
    )

if __name__ == "__main__":
    main()
