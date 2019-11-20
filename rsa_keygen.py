'''
620031587
Net-Centric Computing Assignment
Part A - RSA Encryption
'''

import random
from Crypto.Util import number
import argparse
import math
import message as message_lib
import calculate_power

def generate_big_prime():
    return number.getPrime(16)

def gcd(a, b):
    '''
    Euclid's algorithm for determining the greatest common divisor
    Use iteration to make it faster for larger integers
    '''
    print('Processing Euclid\'algorithm...')
    while b != 0:
        a, b = b, a % b
        # print for debug
        print("a, b = {}, {}".format(a, b))
    return a


def multiplicative_inverse(e, phi):
    '''
    Euclid's extended algorithm for finding the multiplicative inverse of two numbers
    '''
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    print('Processing Euclid\' extended algorithm...')
    while e > 0:
        temp1 = int(temp_phi/e)
        temp2 = temp_phi - temp1 * e
        # print to check error
        #print("{} = {}*{}+{}".format(temp_phi, e, temp1, temp2))
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1
        #print("x={}, y={}".format(x, y))

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

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
    return calculate_power.mod_pow(transformed, e, n)


def decrypt(encrypted, d, n):
    return calculate_power.mod_pow(encrypted, d, n)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-msg', type=str, required=True,
                        help='Input string to crypt')
    args = parser.parse_args()
    print("RSA Encrypter/ Decrypter")
    msg = args.msg

    # chunk message
    messages = []
    chunks = len(msg)
    base = 0
    while chunks > 1:
        messages.append(msg[base:base+6])
        base += 6
        chunks -= 6

    print("Chunked message: ", messages)

    print("Generating your public/private keypairs now . . .")

    # gen private value p q
    print("Generating p and q")
    p = generate_big_prime()
    q = generate_big_prime()
    print('Generated p, q: [', p, ',', q, ']')
    print('Calculating key pair...')

    # gen keys
    public, private = generate_keypair(62483, 49261)
    print("Your public key is ", public, " and your private key is ", private)

    # encrpypt and decrypt message
    with open("encrypted.txt", "w") as encrypt_file, open("decrypted.txt", "w") as decrypt_file:
        encrypt_file.write(str(public[0]) + ' ' + str(public[1]) + '\n')
        decrypt_file.write(str(private[0]) + ' ' + str(private[1]) + '\n')
        for message in messages:
            print("Encrypting: ", message)
            print("Transforming plaintext...")
            transformed = message_lib.transform(message)
            print("Transformed plaintext: ", transformed)
            encrypted = encrypt(transformed, public[0], public[1])
            print("Encrypted message: ", encrypted)
            decrypted = decrypt(encrypted, private[0], private[1])
            print("Decrypted transformed message: ", decrypted)
            print("Plaintext: ", message_lib.detransform(decrypted))
            encrypt_file.write(str(encrypted) + '\n')
            decrypt_file.write(str(message) + '\n')
        encrypt_file.close()
        decrypt_file.close()
    
