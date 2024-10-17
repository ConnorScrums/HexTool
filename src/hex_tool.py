"""Hashing method factory that allows for easy switching of Hashing Methods."""

from typing import Optional
from division_method_hasher import DivisionMethodHasher
from hasher import Hasher
from hash import Hash


class HexTool:
    """Hashing method factory that allows for easy switching of Hashing Methods.

    Attributes:
        division_method_hasher (Hasher)
    """

    def __init__(self) -> None:
        self.__current_hasher: Hasher = None
        self.division_method_hasher: Hasher = DivisionMethodHasher()

    def set_hash_method(self, hash_method: str):
        """Hashing method factory.

        Args:
            hash_method (str): Hash method chosen from the list on the site.

        Todo:
            * Add more hashing methods
        """
        if hash_method == "division-method-hasher":
            self.__current_hasher = self.division_method_hasher
        else:
            self.__current_hasher = None

    def use_hash_method(self, raw_bytes: bytes) -> Optional[Hash]:
        """Hash method user.

        Todo:
            * Add more hashing methods
        """

        if self.__current_hasher:
            return self.__current_hasher(raw_bytes)
        return None
