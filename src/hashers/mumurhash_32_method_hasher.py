"""
Murmurhash 32 implementation, a non-cryptographic
hash function suitable for general hash-based lookup
"""

from .hasher import Hasher
from ..hashes.hash import Hash


class MurmurHash32MethodHasher(Hasher):
    """
    Python implementation of the murmurhash 32 bit x86 algorithm
    """

    def rotl32(self, x, n):
        """Bitwise left rotating the value of x by n positions"""
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    def hash(self, raw_bytes: bytes) -> Hash:
        """
        Murmurhash algorithm implementation
        """
        # constants
        c1 = 0xCC9E2D51
        c2 = 0x1B873593

        # mask python ints to 32 bit ints
        mask = 2**32 - 1

        # seed
        h = 0xE6546B64
        offset = int(len(raw_bytes) / 4)

        # start with chunks of 4 bytes
        for byte in range(0, offset, 4):
            k = byte
            k = (k * c1) & mask
            k = self.rotl32(k, 15) & mask
            k = (k * c2) & mask
            h = (h ^ k) & mask
            h = self.rotl32(h, 13) & mask
            h = h * 5 + 0xE6546B64

        # handle the tail
        tail = len(raw_bytes) & 7
        k1 = 0
        if tail >= 3:
            k1 = k1 ^ (raw_bytes[offset + 2] << 16)

        if tail >= 2:
            k1 = k1 ^ (raw_bytes[offset + 1] << 8)

        if tail >= 1:
            k1 = k1 ^ raw_bytes[offset]
            k1 = (k1 * c1) & mask
            k1 = self.rotl32(k1, 15) & mask
            k1 = (k1 * c2) & mask
            h ^= k1 & mask

        # finalize
        h ^= tail
        h ^= h >> 15
        h *= 0x85EBCA6B
        h ^= h >> 13
        h *= 0xC2B2AE35
        h ^= h >> 15

        return h & mask
