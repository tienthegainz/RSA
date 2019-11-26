from utils import *

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
    'Z': 27,
    ' ': 28
}


def map_character(c, char_to_num=True):
    '''
    map character to number or number to character
    '''
    global switcher
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
    global switcher
    plaintext = plaintext.upper()
    result = 0
    place = len(plaintext) - 1
    for i in range(len(plaintext)):
        result += map_character(plaintext[i],
                                True) * ((len(switcher)+2) ** place)
        place -= 1
    return result


def calculate_length(transformed):
    '''
    get plaintext original length from transformed plaintext 
    '''
    global switcher
    length = 0
    while transformed > (len(switcher)+2):
        length += 1
        transformed /= (len(switcher)+2)
    return length


def detransform(transformed):
    '''
    get original plaintext from transformed plaintext
    '''
    global switcher
    length = calculate_length(transformed)
    message = []
    while length >= 0:
        base = (len(switcher)+2) ** length
        char = int(transformed / base)
        message.append(map_character(char, False))
        transformed -= base * char
        length -= 1
    return ''.join(message)
