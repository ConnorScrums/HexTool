from abc import ABC, abstractmethod
import hash

class Hasher(ABC):
    @abstractmethod
    def hash(self, bytes: bytes) -> hash.Hash:
        pass