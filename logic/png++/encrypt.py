import random
import string

key_length = 4


def transform_key(key):
    new_key = ''

    for c in key:
        c = ord(c)+1
        c %= 256
        new_key += chr(c)

    return new_key


def generate_initial_key():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(4))


def xor(s1, s2):
    res = [chr(0)]*key_length
    for i in range(len(res)):
        q = ord(s1[i])
        d = ord(s2[i])
        k = q ^ d
        res[i] = chr(k)
    res = ''.join(res)
    return res


def add_padding(img):
    l = key_length - len(img)%key_length
    img += chr(l)*l
    return img


def encrypt():
    with open('flag.png', 'rb') as f:
        img = f.read()

    img = add_padding(img)
    key = generate_initial_key()

    enc_data = ''
    for i in range(0, len(img), key_length):
        enc = xor(img[i:i+key_length], key)
        key = transform_key(key)
        enc_data += enc

    with open('encrypted.png', 'wb') as f:
        f.write(enc_data)


def research():
    with open('encrypted.png', 'rb') as f:
        cipher = f.read()

    org = '\x89PNG'
    org += '\x0d\x0a\x1a\x0a'
    org += '\x00\x00\x00\x0d'
    org += 'IHDR'

    keys = []

    for i in xrange(0, len(org), key_length):
        key_used_to_enc = xor(org[i:i+key_length], cipher[i:i+key_length])
        keys.append(key_used_to_enc)

    print keys
    ord_keys = map(lambda key: map(ord, key), keys)
    print ord_keys
    hex_keys = map(lambda key: map(hex, key), ord_keys)
    print hex_keys


def decrypt():
    with open('encrypted.png', 'rb') as f:
        cipher = f.read()

    key = 'IFBY'
    dec_data = ''

    for i in range(0, len(cipher), key_length):
        dec = xor(cipher[i:i + key_length], key)
        key = transform_key(key)
        dec_data += dec

    with open('flag.png', 'wb') as f:
        f.write(dec_data)


decrypt()