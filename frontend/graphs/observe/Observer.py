from abc import ABC, abstractmethod

'''Abstract class that represents an observer object'''
class Observer(ABC):

    # Updates the observer when observable notifies
    @abstractmethod
    def update(self, updated_dict: dict) -> None:
        pass

    '''@abstractmethod
    def getState(self) -> None:
        pass'''
