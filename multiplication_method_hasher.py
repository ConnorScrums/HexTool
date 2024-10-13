from hash import Hash
from hasher import Hasher

class MultiplicationHasher(Hasher):
    def __init__(self) -> None:
        super().__init__()
        self.constant = (7 ** 0.5 - 1) / 2
        self.internal_hashtable = [None for _ in range(self.M_prime)]

    def hash(self, key) -> Hash:
        return 0