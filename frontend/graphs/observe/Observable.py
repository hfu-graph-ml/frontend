from abc import ABC, abstractmethod
import Observer


class Observable(ABC):

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detatch(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify_observer(self) -> None:
        pass
