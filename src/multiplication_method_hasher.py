"""
Adds the remainder of a modulus multiplied by the size of the hash table
to a 64 bit hash, for each byte in the input.
"""

from hash import Hash
from hasher import Hasher
from hash_64_bit import Hash64Bit


class MultiplicationHasher(Hasher):
    """
    For each byte k in the input add h(k) toa a 64-bit hash.
    h(k) is computed as follows: h(k) = floor (M (kA mod 1))
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
