from abc import ABC, abstractmethod
from frontend.graphs.observe import Observer

'''Abstract class that represents an observable object'''
class Observable(ABC):

    # Attaches an observer to the observable object to monitor changes
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    # Detaches an observer
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    # Notifies the observer if changes were recognized
    @abstractmethod
    def notify_observer(self) -> None:
        pass
