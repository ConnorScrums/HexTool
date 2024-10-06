from abc import ABC, abstractmethod

class Hash(ABC):
    def __init__(self, item: any) -> None:
        self.item = item

    @abstractmethod
    def __repr__(self) -> str:
        pass 