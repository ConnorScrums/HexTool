"""Adds the remainder of a modulus to a 64 bit hash, for each byte in the input."""

from hash import Hash
from hash_64_bit import Hash64Bit
from hasher import Hasher


class DivisionMethodHasher(Hasher):
    """Concrete implementation of the Abstract Hasher class that
    takes the modulus of each byte k by M  and adds the remainder to a 64 bit hash."""

    def __init__(self) -> None:
        super().__init__()
        self._m = 97
        self._internal_hashtable = [None for _ in range(self._m)]

    def __call__(self, raw_bytes: bytes) -> Hash:
        """Allows this class to be called as if it were a function."""
        return self.hash(raw_bytes)

    def hash(self, raw_bytes: bytes) -> Hash:
        """Calculates the hash by taking the modulus of each byte and adding it to a 64-bit hash.

        Args:
            raw_bytes (bytes): Array of bytes of the input.

        Returns:
            The hash of the input bytes.
        """
        self.__clear_hashtable()
        res = Hash64Bit(0)

        for byte in raw_bytes:
            hashed_value = byte % self._m
            if self._internal_hashtable[hashed_value] is None:
                self._internal_hashtable[hashed_value] = byte
                res.item += hashed_value
            else:
                i = hashed_value
                placed = False
                for i in range(hashed_value, self._m):
                    if self._internal_hashtable[i] is None:
                        self._internal_hashtable[i] = byte
                        placed = True
                        break
                if not placed:
                    for i in range(0, hashed_value):
                        if self._internal_hashtable[i] is None:
                            self._internal_hashtable[i] = byte
                            placed = True
                            break
                if not placed:
                    self.__clear_hashtable()
                    self._internal_hashtable[hashed_value] = byte
                res.item += hashed_value
        return res

    def __clear_hashtable(self):
        self._internal_hashtable = [None for _ in range(self._m)]
