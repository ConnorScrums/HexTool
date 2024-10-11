"""Abstract Hash Class giving the definition of how a Hash behaves."""

from abc import ABC, abstractmethod


class Hash(ABC):
    """Converts the hash produces by the hasher in a particular bit format."""

    def __init__(self, item: any) -> None:
        self.item = item

    def __repr__(self) -> str:
        return self.to_hash_string()

    @abstractmethod
    def to_hash_string(self) -> str:
        """Abstract method to that determines how a hash is interpreted."""
