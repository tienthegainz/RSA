from Crypto.Util import number


def mod_pow(base, exponent, modulus):
    '''
    calculate modulus of power: (base ^ exponent) % modulus
    '''
    if modulus == 1:
        return 0
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result


def generate_big_prime():
    return number.getPrime(16)


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


def multiplicative_inverse(e, phi):
    '''
    Euclid's extended algorithm for finding the multiplicative inverse of two numbers
    '''
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    # print('Processing Euclid\' extended algorithm...')
    while e > 0:
        temp1 = int(temp_phi/e)
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


def gcd(a, b):
    '''
    Euclid's algorithm for determining the greatest common divisor
    Use iteration to make it faster for larger integers
    '''
    # print('Processing Euclid\'algorithm...')
    while b != 0:
        a, b = b, a % b
    return a


def chunk_message(msg, chunk_size=6):
    '''
        Chunk message into part
        return list of chunked string
    '''
    msg = msg.strip(" \n\t\r")
    messages = []
    chunks = len(msg)
    base = 0
    while chunks > 1:
        messages.append(msg[base:base+chunk_size])
        base += chunk_size
        chunks -= chunk_size
    return messages
