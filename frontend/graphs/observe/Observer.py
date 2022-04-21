from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def getState(self) -> None:
        pass
