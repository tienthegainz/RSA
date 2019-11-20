'''
RSA Cracker
'''

import random
import argparse
import math
import my_crypto
import message as message_lib

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
    parser.add_argument('-f', type=str, required=True, help='file name contain key and encrypted message')
    args = parser.parse_args()
    print("RSA Cracker")
    file = args.f
    with open(file, "r") as encrypted_data:
        lines = encrypted_data.readlines()
        for line in lines:
            if(' ' in line):
                e, n = line.split(' ')
                e = int(e)
                n = int(n)
            else:
                encrypted = int(line)
                print('Message:', line, 'encrypted with key: (', n, ',', e, ')')
                print('Calculating private key....')
                (d, n) = generate_private_key(n, e)
                print('Calculated private key: (', d, ',', n, ')')
                decrypted = my_crypto.decrypt_num_message(line, d, n)
                print("Plaintext: ", message_lib.detransform(decrypted))
    
    
    


    