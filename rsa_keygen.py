'''
620031587
Net-Centric Computing Assignment
Part A - RSA Encryption
'''

import random
import argparse

random.seed(3)


def gcd(a, b):
    '''
    Euclid's algorithm for determining the greatest common divisor
    Use iteration to make it faster for larger integers
    '''
    while b != 0:
        a, b = b, a % b
        # print for debug
        # print("a, b = {}, {}".format(a, b))
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


def is_prime(num):
    '''
    Tests to see if a number is prime.
    '''
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


def generate_keypair(p, q):
    '''
        Gen keypair with p, q
    '''
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
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


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-msg', type=str, default=None,
                        help='Input string to crypt')
    parser.add_argument('-raw', type=str, default=None,
                        help='File path to crypt')
    parser.add_argument('-output', type=str, default=None,
                        help='Encrypted file path')
    parser.add_argument('-p', type=int, required=True,
                        help='Prime number p')
    parser.add_argument('-q', type=int, required=True,
                        help='Prime number q')
    args = parser.parse_args()
    print("RSA Encrypter/ Decrypter")
    p = args.p
    q = args.q
    message = args.msg
    input_file = args.raw
    output_file = args.output
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public,
          " and your private key is ", private)

    with open('key.txt', 'w') as fp:
        fp.write('Public: {}\n'.format(public))
        fp.write('Private: {}\n'.format(private))
        fp.close()

    if message != None:
        encrypted_msg = encrypt(private, message)
        print("Your encrypted message is: ")
        print(''.join(map(lambda x: str(x), encrypted_msg)))
        print("Decrypting message with public key ", public, " . . .")
        print("Your message is:", decrypt(public, encrypted_msg))
    elif input_file != None and output_file != None:
        try:
            ifp = open(input_file, 'r')
            ofp = open(output_file, 'a')
            # read an write
            content = ifp.read()
            print('Content: {}'.format(content))
            # encrypt
            encrypted_msg = encrypt(private, content)
            # print('Encrypted: {}'.format(encrypted_msg))
            ofp.write('{}'.format(
                ''.join(map(lambda x: str(x), encrypted_msg))))
            ifp.close()
            ofp.close()
        except Exception as err:
            print(err)
    else:
        print("Missing argurments")
