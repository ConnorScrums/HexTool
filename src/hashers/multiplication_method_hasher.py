"""
Multiplication Hash which follows the formula `h(K) = floor (M (kA mod 1))`.
"""

from ..hashes.hash import Hash
from ..hashes.hash_64_bit import Hash64Bit
from .hasher import Hasher


class MultiplicationHasher(Hasher):
    """
    1. Choose a constant value A such that 0 < A < 1.
    2. Multiply the key value with A.
    3. Extract the fractional part of kA.
    4. Multiply the result of the above step by the size of the hash table i.e. M.
    5. The resulting hash value is obtained by taking the floor of the result obtained in step 4.

    credits: https://cs.kenyon.edu/index.php/scmp-218-00-data-structures/types-of-hash-functions/
    """

    def __init__(self) -> None:
        super().__init__()
        self.size = 73
        self.constant = (7**0.5 - 1) / 2
        self.internal_hashtable = [None for _ in range(self.size)]

    def __call__(self, raw_bytes: bytes) -> Hash:
        """Allows this class to be called as if it were a function."""
        return self.hash(raw_bytes)

    def hash(self, raw_bytes: bytes) -> Hash:
        self.__clear_hashtable()
        res = Hash64Bit(0)

        for byte in raw_bytes:
            product = float(byte) * self.constant
            frac = product * float(byte) % 1
            hashed_value = int(self.size * frac)
            if self.internal_hashtable[hashed_value] is None:
                self.internal_hashtable[hashed_value] = byte
                res.item += hashed_value
            else:
                i = hashed_value
                placed = False
                for i in range(hashed_value, self.size):
                    if self.internal_hashtable[i] is None:
                        self.internal_hashtable[i] = byte
                        placed = True
                        break
                if not placed:
                    for i in range(0, hashed_value):
                        if self.internal_hashtable[i] is None:
                            self.internal_hashtable[i] = byte
                            placed = True
                            break
                if not placed:
                    self.__clear_hashtable()
                    self.internal_hashtable[hashed_value] = byte
                res.item += hashed_value
        return res

    def __clear_hashtable(self):
        self.internal_hashtable = [None for _ in range(self.size)]
