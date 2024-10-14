from hash import Hash
from hasher import Hasher
from hash_64_bit import Hash64Bit

class MultiplicationHasher(Hasher):
    def __init__(self) -> None:
        super().__init__()
        self.size = 97 # just gonna use the other funcs hash table size
        self.constant = (7 ** 0.5 - 1) / 2
        self.internal_hashtable = [None for _ in range(self.size)]

    def hash(self, key) -> Hash:
        res = Hash64Bit(0)

        product = key * self.constant
        frac = product * int(product)
        res = int(self.size * frac)

        for i in bytes:
            self.internal_hashtable[i] = 0

        return res