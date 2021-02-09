from abc import ABCMeta, abstractmethod


class Connection(metaclass=ABCMeta):

    @abstractmethod
    def put(self, category_id: str, added: str) -> None:
        pass

    @abstractmethod
    def get(self) -> dict:
        pass

    @abstractmethod
    def delete(self, category_id: str) -> None:
        pass

