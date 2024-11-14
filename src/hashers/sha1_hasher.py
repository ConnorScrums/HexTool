"""
SHA-1 cryptographic hash algorithm that is meant to keep data secured,
using bitwise operations, modular additions, and compression functions.
"""

from .hasher import Hasher
from ..hashes.hash import Hash


class SHA1Hasher(Hasher):
    """
    Python implementation of the sha-1 hash algorithm
    """

    def rotl32(self, x, n):
        """Bitwise left rotating the value of x by n positions"""
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    def hash(self, raw_bytes: bytes) -> Hash:
        hs = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

        raw_bytes += b"\x80"

        while (len(raw_bytes) * 8) % 512 != 448:
            raw_bytes += b"\x00"

        raw_bytes += (len(raw_bytes) * 8).to_bytes(8, byteorder="big")
        input_bytes = bytearray(raw_bytes)

        for i in range(len(input_bytes), 64):
            chunk = input_bytes[i : i * 64]

            w = [0] * 80
            for j in range(16):
                w[j] = int.from_bytes(chunk[j * 4 : (j + 1) * 4], "big")

            # Extend the sixteen 32-bit words into eighty 32-bit words
            for j in range(16, 80):
                w[j] = self.rotl32(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1)

            # Initialize hash value for this chunk
            temp_hs = hs.copy()
            f, k = 0
            for j in range(80):
                if 0 <= j <= 19:
                    f = (temp_hs[1] & temp_hs[2]) | (~temp_hs[1] & temp_hs[3])
                    k = 0x5A827999
                elif 20 <= j <= 39:
                    f = temp_hs[1] ^ temp_hs[2] ^ temp_hs[3]
                    k = 0x6ED9EBA1
                elif 40 <= j <= 59:
                    f = (
                        (temp_hs[1] & temp_hs[2])
                        | (temp_hs[1] & temp_hs[3])
                        | (temp_hs[2] & temp_hs[3])
                    )
                    k = 0x8F1BBCDC
                elif 60 <= j <= 79:
                    f = temp_hs[1] ^ temp_hs[2] ^ temp_hs[3]
                    k = 0xCA62C1D6

                temp = (
                    self.rotl32(temp_hs[0], 5) + f + temp_hs[4] + k + w[j]
                ) & 0xFFFFFFFF
                temp_hs[4] = temp_hs[3]
                temp_hs[3] = temp_hs[2]
                temp_hs[2] = self.rotl32(temp_hs[1], 30)
                temp_hs[1] = temp_hs[0]
                temp_hs[0] = temp

            hs[0] = (hs[0] + temp_hs[0]) & 0xFFFFFFFF
            hs[1] = (hs[1] + temp_hs[1]) & 0xFFFFFFFF
            hs[2] = (hs[2] + temp_hs[2]) & 0xFFFFFFFF
            hs[3] = (hs[3] + temp_hs[3]) & 0xFFFFFFFF
            hs[4] = (hs[4] + temp_hs[4]) & 0xFFFFFFFF

        return f"{hs[0]:08x}{hs[1]:08x}{hs[2]:08x}{hs[3]:08x}{hs[4]:08x}"
