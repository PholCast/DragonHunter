from GameElement import GameElement
from abc import ABC, abstractmethod

class GameItem(GameElement,ABC):
    def __init__(self, name, icon,points):
        super().__init__(name, icon) 

        self.points = points
    
    @abstractmethod
    def alterHealth(self):
        pass