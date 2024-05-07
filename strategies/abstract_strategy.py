from abc import ABC, abstractmethod

class HalmaStrategy(ABC):
    
    @abstractmethod
    def move(self, halma_game):
        pass