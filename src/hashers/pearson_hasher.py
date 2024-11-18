"""Pearson Hashing Algorithm"""

import random
from ..hashes.hash import Hash
from ..hashes.hash_64_bit import Hash64Bit
from .hasher import Hasher


class PearsonHasher(Hasher):
    """Pearson hashing is a non-cryptographic hash function designed for fast execution
    on processors with 8-bit registers. Given an input consisting of any number of bytes,
    it produces as output a single byte that is strongly dependent on every byte of the input.

    credit: https://en.wikipedia.org/wiki/Pearson_hashing"""

    def __call__(self, raw_bytes: bytes) -> Hash:
        """Allows this class to be called as if it were a function."""
        return self.hash(raw_bytes)

    def hash(self, raw_bytes: bytes) -> Hash:
        """The Pearson hashing method is designed for 8-bit processes and is a non-crypto
        method of producing a message digest. It produces an 8-bit value which is dependent
        on the data produce. It uses a 256-byte lookup table, and then iterate around the
        bytes in the data.

         Arg:
             raw_bytes (bytes): Array of bytes of the input.

         Returns:
             The hash result of the input bytes after running Pearson Hash
        """
        # Generate a random permutation table
        table = list(range(256))
        random.shuffle(table)

        result_hash = 0
        for byte in raw_bytes:
            result_hash = table[int(result_hash) ^ byte]

        return Hash64Bit(result_hash)
