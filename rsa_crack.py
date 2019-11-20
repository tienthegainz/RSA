'''
RSA Cracker
'''

import random
import argparse
import math
import my_crypto
import message as message_lib
import pickle

def factor(n):
    '''
    find factor of n
    '''
    # find sqrt of n
    c = math.floor(math.sqrt(n))
    if c % 2 == 0:
        c += 1
    # loop all odd number from sqrt of n to 1
    print('Factoring n:')
    for i in range(c, 1, -2):
        print('Pair: [', i, ',', n%i, ']')
        if n % i == 0 and my_crypto.is_prime(i):
            print('Found valid value of p, q: [', i, ',', int(n/i), ']')
            return (i, int(n/i))

def phin(p, q):
    '''
    get phin from p q
    '''
    return (p-1)*(q-1)

def generate_private_key(n, e):
    '''
    get private key from e and phin
    '''
    p, q = factor(n)
    print('Calculating phi(n):')
    phi = phin(p, q)
    print('Calculated phi(n):', phi)
    # Use Extended Euclid's Algorithm to generate the private key

    print('Calculating private key...')
    d = my_crypto.multiplicative_inverse(e, phi)
    return (d, n)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('-msg', type=int, required=True,
    #                     help='Input encrypted message to decrypt')
    # parser.add_argument('-n', type=int, required=True,
    #                     help='Modulus n')
    # parser.add_argument('-e', type=int, required=True,
    #                     help='public key exponent')
    parser.add_argument('-fm', type=str, required=True, help='file data')
    parser.add_argument('-fk', type=str, required=True, help='file name contain key')
    args = parser.parse_args()
    print("RSA Cracker")
    data_file = args.fm
    key_file = args.fk
    try:
        data = open(data_file, "rb")
        key = open(key_file, 'rb')
        data = pickle.load(data)
        key = pickle.load(key)
    except Exception as err:
        print(err)

    print('encrypted with key: e,n ({}, {})'.format(key['public'][0], key['public'][1]))
    e = key['public'][0]
    n = key['public'][1]
    #exit()
    print('Calculating private key....')
    (d, n) = generate_private_key(n, e)
    print('Calculated private key: (', d, ',', n, ')')
    base = []
    for line in data:
        decrypted = my_crypto.decrypt_num_message(line, d, n)
        base.append(message_lib.detransform(decrypted))
        # print("Plaintext: ", message_lib.detransform(decrypted))
    print(''.join(base))
    
    
    


    