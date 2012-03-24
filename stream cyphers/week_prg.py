#!/usr/bin/env python

import random

P = 295075153L   # about 2^28

class WeakPrng(object):
    def __init__(self, p):   # generate seed with 56 bits of entropy
        self.p = p
        self.x = random.randint(0, p)
        self.y = random.randint(0, p)
   
    def next(self):
        # x_{i+1} = 2*x_{i}+5  (mod p)
        self.x = (2*self.x + 5) % self.p

        # y_{i+1} = 3*y_{i}+7 (mod p)
        self.y = (3*self.y + 7) % self.p

        # z_{i+1} = x_{i+1} xor y_{i+1}
        return (self.x ^ self.y) 

solve = [210205973, 22795300, 58776750, 121262470, 264731963, 140842553, 242590528, 195244728, 86752752]

base_num = solve[0];

counter = 0L
border = 2145902400L*256L
while counter < border:
    seed = counter
    random.seed(seed)
    prng = WeakPrng(P)
    if base_num == prng.next():
        print "Seed found", seed
    counter = counter+1L
