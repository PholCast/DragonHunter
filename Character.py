from abc import ABC, abstractmethod
from GameElement import GameElement
class Character(GameElement,ABC):
    def __init__(self,name,icon,position = None,health = None):
        super().__init__(name, icon)
        self.position = position
        self.health = health
    
    @abstractmethod
    def move(self):
        pass
    
    @abstractmethod
    def attack(self):
        pass

    def isDead(self):
        if self.health <= 0:
            return True
        else:
            return False

    def printCharacterInfo(self):
        print(f"Datos del {self.name} {self.icon}:\tPosicion: {self.position}\tVida:{self.health}\n")


    

    #crear un position (x,y)