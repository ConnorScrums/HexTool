"""Hashing method factory that allows for easy switching of Hashing Methods."""

from typing import Optional
from .hashers.division_method_hasher import DivisionMethodHasher
from .hashers.multiplication_method_hasher import MultiplicationHasher
from .hashers.mumurhash_32_method_hasher import MurmurHash32MethodHasher
from .hashers.hasher import Hasher
from .hashes.hash import Hash


class HexTool:
    """Hashing method factory that allows for easy switching of Hashing Methods.

    Attributes:
        division_method_hasher (Hasher)
    """

    def __init__(self) -> None:
        self.__current_hasher: Hasher = None
        self.division_method_hasher: Hasher = DivisionMethodHasher()
        self.multiplication_method_hasher: Hasher = MultiplicationHasher()
        self.murmurhash_32_method_hasher: Hasher = MurmurHash32MethodHasher()

    def set_hash_method(self, hash_method: str):
        """Hashing method factory.

        Args:
            hash_method (str): Hash method chosen from the list on the site.

        Todo:
            * Add more hashing methods
        """
        if hash_method == "division-method-hasher":
            self.__current_hasher = self.division_method_hasher
        elif hash_method == "multiplication-method-hasher":
            self.__current_hasher = self.multiplication_method_hasher
        elif hash_method == "murmurhash-32-method-hasher":
            self.__current_hasher = self.murmurhash_32_method_hasher
        else:
            self.__current_hasher = None

    def use_hash_method(self, raw_bytes: bytes) -> Optional[Hash]:
        """Hash method user."""

        if self.__current_hasher:
            return self.__current_hasher(raw_bytes)
        return None
