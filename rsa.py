import random
import math

def setkeys():
    p = 67
    q = 71
    n = p * q
    phi_n = (p - 1) * (q - 1)
    eValues = [e for e in range(2, phi_n) if math.gcd(e, phi_n) == 1]
    e = random.choice(eValues)
    publicKey = e
    d = 2
    while True:
        if (d * e) % phi_n == 1:
            break
        d += 1
    privateKey = d
    return publicKey, privateKey, n

def encrypt(message, publicKey, n):
    e = publicKey
    encrypted_text = 1
    while e > 0:
        encrypted_text *= message
        encrypted_text %= n
        e -= 1
    return encrypted_text

def encoder(message, publicKey, n):
    encoded = []
    for letter in message:
        encoded.append(encrypt(ord(letter), publicKey, n))
    return encoded

def decrypt(encrypted_text, privateKey, n):
    d = privateKey
    decrypted = 1
    while d > 0:
        decrypted *= encrypted_text
        decrypted %= n
        d -= 1
    return decrypted

def decoder(encoded, privateKey, n) :
    s = ''
    for num in encoded:
        s += chr(decrypt(num, privateKey, n))
    return s