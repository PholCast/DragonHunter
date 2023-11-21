import random
from Character import Character

class Enemy(Character):
    def __init__(self, name="Enemy", icon="🐉", position = None,health = 100):
        super().__init__(name,icon,position,health)
        self.damage = -25
    
    def move(self):
        moves = ["up","down","left","right"]
        return random.choice(moves)


    def attack(self):
        print("Enemy te ha atacado!")
        return self.damage

        
        
