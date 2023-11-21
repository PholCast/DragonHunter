from Food import Food
from Weapon import Weapon
class ItemCreator:

    foodData = {
                "apple": {"name": "Aguacate", "icon": "🥑", "points": 10},
                "chicken_leg": {"name": "Chicken Leg", "icon": "🍗", "points": 20},
                "pizza": {"name": "Pizza", "icon": "🍕", "points": 18},
                "hamburger": {"name": "Hamburger", "icon": "🍔", "points": 22},
                }

    weaponData ={
                "machete": {"name": "machete", "icon": "🔪", "points": -20, "range": "short"},
                "bow": {"name": "Bow", "icon": "🏹", "points": -15, "range": "medium"},
                "bomb": {"name": "bomb", "icon": "💣", "points": -18, "range": "long"},
                "pistol": {"name": "Pistol", "icon": "🔫", "points": -22, "range": "medium"},
                 }

    @staticmethod
    def createFood() -> [Food]:
        foodList = []
        for food in ItemCreator.foodData.keys():

            name = ItemCreator.foodData[food]["name"]
            icon = ItemCreator.foodData[food]["icon"]
            points = ItemCreator.foodData[food]["points"]

            foodObject = Food(name,icon,points)
            
            foodList.append(foodObject)
        
        return foodList

        
    
    @staticmethod
    def createWeapons() -> [Weapon]:
        weaponList = []
        
        for weapon in ItemCreator.weaponData.keys():

            weaponName = ItemCreator.weaponData[weapon]["name"]
            weaponIcon = ItemCreator.weaponData[weapon]["icon"]
            points = ItemCreator.weaponData[weapon]["points"]
            weaponRange = ItemCreator.weaponData[weapon]["range"]

            foodObject = Weapon(weaponName,weaponIcon,points,weaponRange)
            
            weaponList.append(foodObject)
        
        return weaponList