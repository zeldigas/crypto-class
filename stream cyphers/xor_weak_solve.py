#!/usr/bin/env python
P = 295075153L   # about 2^28

class WeakPrng(object):
    def __init__(self, p, x_guess):   # generate seed with 56 bits of entropy
        self.p = p
        self.x = x_guess
        self.y = 210205973L ^ self.x
   
    def next(self):
        # x_{i+1} = 2*x_{i}+5  (mod p)
        self.x = (2*self.x + 5) % self.p

        # y_{i+1} = 3*y_{i}+7 (mod p)
        self.y = (3*self.y + 7) % self.p

        # z_{i+1} = x_{i+1} xor y_{i+1}
        return (self.x ^ self.y) 

solve = [210205973, 22795300, 58776750, 121262470, 264731963, 140842553, 242590528, 195244728, 86752752]

#base_num = solve[1]

#counter = 0L
#border = P
#while counter < border:
#    prng = WeakPrng(P, counter)
#    if base_num == prng.next():
#        print "X_guess found", counter
#    if counter % 100000 == 0:
#        print "Processed guesses", counter, "need to process", border - counter
#    counter = counter+1L

guess_x = [89059908, 189093025, 268575982]

for x in guess_x:
    prng = WeakPrng(P, x)
    gen = [prng.next() for i in range(len(solve)-1)]
    if gen == solve[1:]:
        print "X=%d is a solve, next element in sequence %d" %(x, prng.next())


