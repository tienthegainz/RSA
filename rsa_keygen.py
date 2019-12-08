'''
620031587
Net-Centric Computing Assignment
Part A - RSA Encryption
'''

import random
from Crypto.Util import number
import argparse
import math
import pickle

from utils import *
from rsa_utils import *

random.seed(3)


def generate_keypair(p, q):
    '''
        Gen keypair with p, q
    '''
    #n = pq
    n = p * q

    # Phi is the totient of n
    phi = (p-1) * (q-1)

    # Choose an integer e such that e and phi(n) are coprime
    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    while True:
        e = random.randrange(2, phi)
        #print("--> ", e, phi)
        if gcd(phi, e) == 1:
            break

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(transformed, e, n):
    return mod_pow(transformed, e, n)


def decrypt(encrypted, d, n):
    return mod_pow(encrypted, d, n)


def rsa_encrypt(content, p=None, q=None, e=None, n=None):
    messages = chunk_message(content)
    if e != None and n != None:
        public = (e, n)
        print('Pre-defined key: ({})\n'.format(public))
    else:
        if p == None or q == None:
            p = generate_big_prime()
            q = generate_big_prime()
        public, _ = generate_keypair(p, q)

    encrypt_msg = list()
    for message in messages:
        transformed = transform(message)
        encrypted = encrypt(transformed, public[0], public[1])
        encrypt_msg.append(encrypted)

    return public, encrypt_msg


if __name__ == '__main__':
    key, code = rsa_encrypt('Hello boys It was me Dio')
    print('Key: {}'.format(key))
    print('Code: {}'.format(code))
