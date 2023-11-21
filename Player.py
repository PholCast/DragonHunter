from Character import Character
from Food import Food
from Weapon import Weapon
import time
from FaceDetection import FaceDetection


class Player(Character):
    def __init__(self, name="Player", icon="🤠", position = None,health = 10):
        super().__init__(name,icon,position,health)
        self.inventory = {"Food":[],"Weapons":[]}
    
    def printCharacterInfo(self):
        super().printCharacterInfo()
        print(f"Inventario de Comida: {self.inventory['Food']}")
        print(f"Inventario de Armas: {self.inventory['Weapons']}\n")



    def chooseWeapon(self,cam) -> Weapon :
        print("Tus armas son: ",end="\t")
        for weapon in self.inventory["Weapons"]:
            print(f"{weapon}  ")
        print("\n")

        #FaceDetection
        #indexWeapon = int(input("Selecciona un arma: "))
        print("Cuando tengas seleccionada el arma, mira hacia arriba")
        indexWeapon = self.chooseIndexOption(cam,self.inventory["Weapons"])

        chosenWeapon = self.inventory["Weapons"][indexWeapon]

        return chosenWeapon
    


    def chooseIndexOption(self,cam,collection,action ="up"):
        index = 0
        print("Parpadea o sonrie para cambiar de opcion:")
        print("Indice actual:  ",index)
        print("Estas en la posicion de: ",collection[index] )
        #parpadear para sumar, sonreir para restar
        while True:
            time.sleep(1)
            FaceDetection.detect(cam)

            if FaceDetection.playerAction == "closed eyes":
                index +=1
                if index == len(collection):
                    index = 0
            elif FaceDetection.playerAction == "smile":
                index -=1
                if index == -1:
                    index = len(collection)-1

            elif FaceDetection.playerAction == action:
                break
            FaceDetection.playerAction = None
                

            print("Indice actual:  ",index)
            print("Estas en la posicion de: ",collection[index] )
        
        print("Escogiste: ",collection[index])
        FaceDetection.playerAction = None
        time.sleep(2)
        return index
    



    def move(self):
        pass
    def attack(self,enemyPosition,cam):
        if len(self.inventory["Weapons"]) == 0:
            print("No tienes armas para atacar")
            return 0
        
        
        
        chosenWeapon = self.chooseWeapon(cam)

        ranges = {"short": 0, "medium": 2, "long": 4}

        numWeaponRange = ranges[chosenWeapon.weaponRange]

        if self.canAttack(self.position,enemyPosition,numWeaponRange):
            print(f"Has atacado al monstruo con {chosenWeapon}")
            return chosenWeapon.points
        else:
            print(f"No puedes atacar con {chosenWeapon} porque es de rango {chosenWeapon.weaponRange}: {numWeaponRange}")
            return 0
        
    
    def canAttack(self,playerPosition,enemyPosition,range):

        if playerPosition == enemyPosition:
            return True
        
        if range == 0:
            return False
        

        up = [playerPosition[0]-1,playerPosition[1]]

        down = [playerPosition[0]+1,playerPosition[1]]

        left = [playerPosition[0],playerPosition[1]-1]

        right = [playerPosition[0],playerPosition[1]+1]
        
                                        #up                                     #down                                #left                                      #right
        return self.canAttack(up,enemyPosition,range-1) or self.canAttack(down,enemyPosition,range-1) or self.canAttack(left,enemyPosition,range-1) or self.canAttack(right,enemyPosition,range-1)

    def addToInventory(self,item):
        if isinstance(item,Food):
            self.inventory["Food"].append(item)
        else:
            self.inventory["Weapons"].append(item)
        
        print(f"{item} se ha agregado al inventario")


    def eat(self,cam):
        #FaceDetection
        if len(self.inventory["Food"]) == 0:
            print("No hay alimentos disponibles en el inventario")
            return False
        else:
            print("Cuando tengas seleccionado el snack, abre la boca para comer")
            indexSnack = self.chooseIndexOption(cam,self.inventory["Food"],"open mouth")
            # elegir con el FaceDetection
            #por ahora pondré un numero random xd
            snack = self.inventory["Food"].pop(indexSnack)
            self.health +=snack.points
            print(f"Comiste {snack}. Tu salud ha aumentado {snack.points} puntos")
            return True
        
        
