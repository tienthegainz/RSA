import calculate_power
import random

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

def decrypt_num_message(msg, d, n):
    '''
    decrypt encrypted message with private key calculated
    '''
    return calculate_power.mod_pow(msg, d, n)

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