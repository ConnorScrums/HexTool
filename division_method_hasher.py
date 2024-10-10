from hash import Hash
from hash_64_bit import Hash64Bit
from hasher import Hasher


class DivisionMethodHasher(Hasher):
    def __init__(self) -> None:
        super().__init__()
        self.M_prime = 97
        self.internal_hashtable = [None for _ in range(self.M_prime)]

    def hash(self, bytes: bytes) -> Hash:
        self.clear_hashtable()
        res = Hash64Bit(0)

        for byte in bytes:
            hashed_value = byte % self.M_prime
            if self.internal_hashtable[hashed_value] is None:
                self.internal_hashtable[hashed_value] = byte
                res.item += hashed_value
            else:
                i = hashed_value
                placed = False
                for i in range(hashed_value, self.M_prime):
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
                    self.clear_hashtable()
                    self.internal_hashtable[hashed_value] = byte
                res.item += hashed_value
        return res

    def clear_hashtable(self):
        self.internal_hashtable = [None for _ in range(self.M_prime)]