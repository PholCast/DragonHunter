from GameItem import GameItem

class Food(GameItem):
    def __init__(self,name,icon,points):
        super().__init__(name,icon,points)
    
    def alterHealth(self):
        pass

        