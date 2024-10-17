from division_method_hasher import DivisionMethodHasher
from multiplication_method_hasher import MultiplicationHasher
from hasher import Hasher


class HexTool:
    def __init__(self) -> None:
        self.division_method_hasher = DivisionMethodHasher()
        self.multiplication_method_hasher = MultiplicationHasher()

    def get_hash_method(self, hash_method: str) -> Hasher:
        ## TODO :: Add more hashing methods
        if hash_method == "division-method-hasher":
            return self.division_method_hasher
        elif hash_method == "multiplication-method-hasher":
            return self.multiplication_method_hasher
        elif hash_method == "":
            pass