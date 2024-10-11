"""Abstract Hasher Class giving the definition of how a Hasher behaves."""

from abc import ABC, abstractmethod
from hash import Hash


class Hasher(ABC):
    """Abstract Hasher Class giving the definition of how a Hasher behaves."""

    def __call__(self, raw_bytes: bytes) -> Hash:
        """Allows this class to be called as if it were a function."""
        return self.hash(raw_bytes)

    @abstractmethod
    def hash(self, raw_bytes: bytes) -> Hash:
        """Calculates the hash by a concrete method for each byte and adding it to an N-bit hash.

        Args:
            raw_bytes (bytes): Array of bytes of the input.

        Returns:
            The hash of the input bytes.
        """
