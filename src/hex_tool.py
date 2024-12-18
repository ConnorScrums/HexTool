"""Hashing method factory that allows for easy switching of Hashing Methods."""

from typing import Optional
from .hashers.division_method_hasher import DivisionMethodHasher
from .hashers.multiplication_method_hasher import MultiplicationHasher
from .hashers.mumurhash_32_method_hasher import MurmurHash32MethodHasher
from .hashers.folding_method_hasher import FoldingMethodHasher
from .hashers.mid_square_method_hasher import MidSquareHasher
from .hashers.pearson_hasher import PearsonHasher
from .hashers.sha1_hasher import SHA1Hasher
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
        self.folding_method_hasher: Hasher = FoldingMethodHasher()
        self.mid_square_method_hasher: Hasher = MidSquareHasher()
        self.pearson_method_hasher: Hasher = PearsonHasher()
        self.sha1_method_hasher: Hasher = SHA1Hasher()

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
        elif hash_method == "folding-method-hasher":
            self.__current_hasher = self.folding_method_hasher
        elif hash_method == "mid-square-method-hasher":
            self.__current_hasher = self.mid_square_method_hasher
        elif hash_method == "pearson-method-hasher":
            self.__current_hasher = self.pearson_method_hasher
        elif hash_method == "sha-1-method-hasher":
            self.__current_hasher = self.sha1_method_hasher
        else:
            self.__current_hasher = None

    def use_hash_method(self, raw_bytes: bytes) -> Optional[Hash]:
        """Hash method user."""

        if self.__current_hasher:
            return self.__current_hasher(raw_bytes)
        return None
