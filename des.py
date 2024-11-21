import table as t

def binaryString(binaryText):
    string = ''.join(binaryText)
    text = ""
    for i in range(0, len(string), 8):
        char_binary = string[i:i+8]
        try:
            char = chr(int(char_binary, 2))
            if not (32 <= ord(char) <= 126):
                text += ' '
            else:
                text += char
        except ValueError:
            text += ' '
    return text

def binaryHex(binaryText):
    hexNumber = format(int(binaryText, 2), 'X')
    return hexNumber

def stringBinary(text):
    binaryText = ""
    for char in text:
        binaryChar = bin(ord(char))[2:].zfill(8)
        binaryText += binaryChar
    padding = (64 - len(binaryText) % 64) % 64
    binaryText += '0' * padding
    return [binaryText[i:i+64] for i in range(0, len(binaryText), 64)]

def decimalBinary(decimal):
    if decimal == 0:
        return "0000"
    binaryText = ""
    while decimal > 0:
        binaryText = str(decimal % 2) + binaryText
        decimal //= 2
    while len(binaryText) < 4:
        binaryText = '0' + binaryText
    return binaryText

def xor(a, b):
    length = max(len(a), len(b))
    a = a.zfill(length)
    b = b.zfill(length)
    result = ''
    for i in range(length):
        if a[i] == b[i]:
            result += '0'
        else:
            result += '1'
    return result

def permute(source, table):
    result = ""
    for i in table:
        result += source[i - 1]
    return result

def leftShift(key, shift):
    return key[shift:] + key[:shift]

def generateKeys(key):
    roundKeys = []
    key1 = permute(key, t.keyParity)
    left = key1[0:28]
    right = key1[28:56]
    for i in range(0, 8):
        left = leftShift(left, t.leftShifts[i])
        right = leftShift(right, t.leftShifts[i])
        roundKey = permute(left + right, t.keyCompression)
        roundKeys.append(roundKey)
    return roundKeys

def encrypt(plaintext, roundKeys):
    newPlainText = permute(plaintext, t.initialPermutation)
    left = newPlainText[0:32]
    right = newPlainText[32:64]
    for i in range(0, 8):
        expandRight = permute(right, t.expansionDBox)
        xorRight = xor(expandRight, roundKeys[i])
        sboxRight = ""
        for j in range(0, 48, 6):
            chunk = xorRight[j:j + 6]
            row = int(chunk[0] + chunk[5], 2)
            col = int(chunk[1:5], 2)
            sboxRight += decimalBinary(t.sBox[j//6][row][col])
        straightpRight = permute(sboxRight, t.straightPermutation)
        result = xor(left, straightpRight)
        left = right
        right = result
    cipher_text = permute((right + left), t.finalPermutation)
    return cipher_text

def decrypt(ciphertext, roundKeys):
    rev_roundKeys = roundKeys[::-1]
    return encrypt(ciphertext, rev_roundKeys)