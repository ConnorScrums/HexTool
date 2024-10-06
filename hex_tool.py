from division_method_hasher import DivisionMethodHasher
from hasher import Hasher


class HexTool:
    def __init__(self) -> None:
        self.division_method_hasher = DivisionMethodHasher()

    def get_hash_method(self, hash_method: str) -> Hasher:
        ## TODO :: Add more hashing methods
        if hash_method == "division-method-hasher":
            return self.division_method_hasher
        elif hash_method == "":
            pass