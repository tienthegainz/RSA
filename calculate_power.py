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