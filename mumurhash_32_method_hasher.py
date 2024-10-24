"""
Murmurhash 32 implementation, a non-cryptographic 
hash function suitable for general hash-based lookup
"""
from hash import Hash
from hasher import Hasher

class MurmurHash32MethodHasher(Hasher):
    """
    Python implementation of the murmurhash 32 bit x86 algorithm
    """
    def __init__(self) -> None:
        """Initialize"""
        super().__init__()

    def rotl32(self, x, n):
        """Bitwise left rotating the value of x by n positions"""
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    def hash(self, bytes: bytes) -> Hash:
        """
        Murmurhash algorithm implementation
        """
        #constants
        c1 = 0xcc9e2d51
        c2 = 0x1b873593

        #mask python ints to 32 bit ints
        mask = 2 ** 32 - 1

        #seed
        h = 0xe6546b64
        offset = int(len(bytes)/4)

        #start with chunks of 4 bytes
        for byte in range(0, offset, 4):
            k = byte
            k = (k * c1) & mask
            k = self.rotl32(k, 15) & mask
            k = (k * c2) & mask
            h = (h ^ k) & mask
            h = self.rotl32(h, 13) & mask
            h = h * 5 + 0xe6546b64

        #handle the tail
        l = len(bytes) & 7
        k1 = 0
        if l >= 3:
            k1 = k1 ^ (bytes[offset+2] << 16)

        if l >= 2:
            k1 = k1 ^ (bytes[offset+1] << 8)

        if l >= 1:
            k1 = k1 ^ bytes[offset]
            k1 = (k1 * c1) & mask
            k1 = self.rotl32(k1, 15) & mask
            k1 = (k1 * c2) & mask
            h ^= k1 & mask

        #finalize
        h ^= l
        h ^= h >> 15
        h *= 0x85ebca6b
        h ^= h >> 13
        h *= 0xc2b2ae35
        h ^= h >> 15

        return h & mask
