from GameItem import GameItem

class Weapon(GameItem):
    def __init__(self,name,icon,points,WRange):
        super().__init__(name,icon,points)
        
        self.weaponRange = WRange
        
    
    def alterHealth(self):
        pass


    #Player will be able to attack based on the range
    def canAttack(self):
        pass 