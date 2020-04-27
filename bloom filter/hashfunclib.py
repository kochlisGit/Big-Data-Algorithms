import binascii
import hashlib
import random as rand

def crc32(string):
    return binascii.crc32( string.encode() )

def murmur3_32(string, seed = 0):
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    length = len(string)
    h1 = seed
    roundedEnd = (length & 0xfffffffc)
    for i in range(0, roundedEnd, 4):

      k1 = (ord(string[i]) & 0xff) | ((ord(string[i + 1]) & 0xff) << 8) | \
           ((ord(string[i + 2]) & 0xff) << 16) | (ord(string[i + 3]) << 24)
      k1 *= c1
      k1 = (k1 << 15) | ((k1 & 0xffffffff) >> 17)
      k1 *= c2

      h1 ^= k1
      h1 = (h1 << 13) | ((h1 & 0xffffffff) >> 19)
      h1 = h1 * 5 + 0xe6546b64

    k1 = 0
    val = length & 0x03
    if val == 3:
        k1 = (ord(string[roundedEnd + 2]) & 0xff) << 16

    if val in [2, 3]:
        k1 |= (ord(string[roundedEnd + 1]) & 0xff) << 8

    if val in [1, 2, 3]:
        k1 |= ord(string[roundedEnd]) & 0xff
        k1 *= c1
        k1 = (k1 << 15) | ((k1 & 0xffffffff) >> 17)
        k1 *= c2
        h1 ^= k1

    h1 ^= length
    h1 ^= ((h1 & 0xffffffff) >> 16)
    h1 *= 0x85ebca6b
    h1 ^= ((h1 & 0xffffffff) >> 13)
    h1 *= 0xc2b2ae35
    h1 ^= ((h1 & 0xffffffff) >> 16)

    return h1 & 0xffffffff

def fnv_1a(string):
    FNV1A_32_OFFSET = 0x811c9dc5
    FNV1A_32_PRIME = 0x01000193
    h = FNV1A_32_OFFSET

    for ch in string:
        h ^= ord(ch)
        h *= FNV1A_32_PRIME
        h &= 0xffffffff
    return h

def djb2(string):                                                                                                                                
    h = 5381
    for ch in string:
        h = (( h << 5) + h) + ord(ch)
    return h & 0xFFFFFFFF

def sha256(string):
    hash_bytes = hashlib.sha256( string.encode('utf-8') ).digest()
    first_bytes = hash_bytes[:8]
    return int.from_bytes(first_bytes, byteorder="little", signed=False)