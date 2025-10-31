from abc import ABC, abstractmethod


class SortingStrategy(ABC):
    @abstractmethod
    def isReady(self, objs):
        pass

    @abstractmethod
    def perform(self, objs):
        pass

    @abstractmethod
    def isComplete(self, objs):
        pass
