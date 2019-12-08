'''
RSA Cracker
'''

import random
import argparse
import math
import pickle
from utils import *
from rsa_utils import *


def factor(n):
    '''
    find factor of n
    '''
    # find sqrt of n
    c = math.floor(math.sqrt(n))
    if c % 2 == 0:
        c += 1
    # loop all odd number from sqrt of n to 1
    #print('Factoring n:')
    for i in range(c, 1, -2):
        # print('Pair: [', i, ',', n % i, ']')
        if n % i == 0 and is_prime(i):
            #print('Found valid value of p, q: [', i, ',', int(n/i), ']')
            return (i, int(n/i))


def phin(p, q):
    '''
    get phin from p q
    '''
    return (p-1)*(q-1)


def decrypt_num_message(msg, d, n):
    '''
    decrypt encrypted message with private key calculated
    '''
    return mod_pow(msg, d, n)


def generate_private_key(n, e):
    '''
    get private key from e and phin
    '''
    p, q = factor(n)
    #print('Calculating phi(n):')
    phi = phin(p, q)
    #print('Calculated phi(n):', phi)
    # Use Extended Euclid's Algorithm to generate the private key

    #print('Calculating private key...')
    d = multiplicative_inverse(e, phi)
    return (d, n)


def rsa_decrypt(public, data):
    e = public[0]
    n = public[1]
    # print('n = {} -- e = {}'.format(n, e))
    (d, n) = generate_private_key(n, e)
    print('Found: d = {} -- n = {}'.format(d, n))
    base = []
    for line in data:
        decrypted = decrypt_num_message(line, d, n)
        print("Decrypted: {}\n".format(detransform(decrypted)))
        base.append(detransform(decrypted))

    return (''.join(base), (d, n))


if __name__ == '__main__':
    data = [235166692, 2110155522, 125573377, 915470449]
    key = (1022050303, 2735284621)
    message = rsa_decrypt(key, data)
    print(message)
