from abc import ABC, abstractmethod


class TransactionOutputPort[T](ABC):
    @abstractmethod
    def write(self, items: list[T]) -> None:
        """Persist or publish items to an output destination."""
