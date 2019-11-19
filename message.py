

def map_character(c, char_to_num = True):
    '''
    map character to number or number to character
    '''
    switcher = { 
        'A': 2, 
        'B': 3, 
        'C': 4, 
        'D': 5,
        'E': 6,
        'F': 7,
        'G': 8,
        'H': 9,
        'I': 10,
        'J': 11,
        'K': 12,
        'L': 13,
        'M': 14,
        'N': 15,
        'O': 16,
        'P': 17,
        'Q': 18,
        'R': 19,
        'S': 20,
        'T': 21,
        'U': 22,
        'V': 23,
        'W': 24,
        'X': 25,
        'Y': 26,
        'Z': 27
    } 

    if char_to_num == True:
        return switcher.get(c)
    else:
        for key, value in switcher.items():
            if c == value:
                return key


def transform(plaintext):
    '''
    transform plaintext into number
    '''
    result = 0
    place = len(plaintext) - 1
    for i in range(len(plaintext)):
        result += map_character(plaintext[i]) * (26 ** place)
        place -= 1
    return result

def calculate_length(transformed):
    '''
    get plaintext original length from transformed plaintext 
    '''
    len = 0
    while transformed > 26:
        len += 1
        transformed /= 26
    return len

def detransform(transformed):
    '''
    get original plaintext from transformed plaintext
    '''
    len = calculate_length(transformed)
    message = []
    while len >= 0:
        base = 26 ** len
        char = int(transformed / base)
        message.append(map_character(char, False))
        transformed -= base * char
        len -= 1
    return ''.join(message)