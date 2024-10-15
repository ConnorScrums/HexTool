from hash import Hash
from hasher import Hasher
from hash_64_bit import Hash64Bit

class MultiplicationHasher(Hasher):
    def __init__(self) -> None:
        super().__init__()
        self.size = 97 # just gonna use the other funcs hash table size
        self.constant = (7 ** 0.5 - 1) / 2
        self.internal_hashtable = [None for _ in range(self.size)]

    def hash(self, bytes: bytes) -> Hash:
        res = Hash64Bit(0)

        for byte in bytes:
            product = bytes * self.constant
            frac = product * int(product)
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
                    self.clear_hashtable()
                    self.internal_hashtable[hashed_value] = byte
                res.item += hashed_value
        return res
    

    def clear_hashtable(self):
        self.internal_hashtable = [None for _ in range(self.size)]