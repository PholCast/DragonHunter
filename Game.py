from Weapon import Weapon
from Player import Player
from Enemy import Enemy
import cv2
from Food import Food
from ItemCreator import ItemCreator
import random
from Character import Character
from GameItem import GameItem
import os

import time


from FaceDetection import FaceDetection

class Game:
    
    food = ItemCreator.createFood()

    weapons = ItemCreator.createWeapons()

    matrix = [] # hacer que mostrando cierta cantidad de dedos cree el size de la matriz seria buena idea

    player = None

    enemy = None

    turn = None

    cam = cv2.VideoCapture(0)

    @staticmethod
    def clearConsole():
        os.system("cls")

    # , requestMove,
    @staticmethod
    def printInfoGame():
        for row in Game.matrix:
            print(row)
        Game.player.printCharacterInfo()
        Game.enemy.printCharacterInfo()


    @staticmethod
    def play():
        while(True):
            Game.printInfoGame()

            if Game.turn == Game.player:

                time.sleep(2)
                #FaceDetection here
                Game.requestAction() #request move player            

            else: #enemy's turn
                while(True):

                    move = Game.enemy.move()

                    if Game.moveCharacter(move): #if move is valid, continue
                        break

                if Game.turn.position == Game.player.position:
                    Game.player.health+= Game.enemy.attack()

            if Game.verifyWinner():
                print("🔥🔥🔥🔥🔥🔥🔥🔥🔥")
                Game.printInfoGame()
                print("🔥🔥🔥🔥🔥🔥🔥🔥🔥")

                break
            
            Game.switchTurn()

    @staticmethod
    def requestAction():
        #FaceDetection Here
        valid = False
        while(not valid):
            print("Que harás?")
            while FaceDetection.playerAction == None:
                FaceDetection.detect(Game.cam)
            #action = int(input("Que harás?:\n1. Mover\n2.Comer\n3.Agregar a Inventario\n4.Atacar Con arma del inventario"))

            #if action == 1:
            action = FaceDetection.playerAction

            FaceDetection.playerAction = None

            if action == "up": #moverse
                while(True):
                    print("Elegiste mover")
                    time.sleep(2)
                    #movement = input("hacia donde te vas a mover? (up,down,left,right)") #aqui podría llamar al metodo del player y que se haga con FaceDetection
                    

                    while(True):
                        print("hacia donde te vas a mover? (up,down,left,right)")
                        FaceDetection.detect(Game.cam)
                        move = FaceDetection.playerAction
                        if move in ["up","down","left","right"]:
                            break
                        FaceDetection.playerAction = None

                    movement = FaceDetection.playerAction

                    if Game.moveCharacter(movement):
                        break
                    FaceDetection.playerAction = None
                valid = True
                print("Te has movido")
            elif action == "open mouth": #comer
                time.sleep(2)
                print("Elegiste comer")
                valid = Game.turn.eat(Game.cam)
            elif action == "smile": #Agregar Inventario
                print("Elegiste agregar a inventario")
                time.sleep(2)
                currentPosition = Game.matrix[Game.turn.position[0]][Game.turn.position[1]]

                if type(currentPosition) == list:
                    if isinstance(currentPosition[0],GameItem):
                        Game.turn.addToInventory(currentPosition[0])
                        currentPosition.pop(0)

                        if len(currentPosition) == 1:
                            currentPosition = currentPosition[0]
                        
                        Game.matrix[Game.turn.position[0]][Game.turn.position[1]] = currentPosition
                        valid = True
                        

                    else:
                        print("No hay Items en tu posicion actual")
                        valid = False
                else:
                    print("No hay Items en tu posicion actual")
                    valid = False
            
            elif action == "left": #Atacar
                print("elegiste atacar")
                time.sleep(2)
                damage = Game.turn.attack(Game.enemy.position,Game.cam)

                #si el damage es diferente de cero es porque si pudo atacar
                if damage != 0:
                    Game.enemy.health+=damage
                    valid = True
                else:
                    valid = False
            
            FaceDetection.playerAction = None
        Game.clearConsole()


    @staticmethod
    def moveCharacter(move):
        movements = {"up" : [-1,0], "down" : [1,0], "left" : [0,-1], "right" : [0,1]}
        currentPosition = Game.turn.position

        x = movements[move][0]
        y = movements[move][1]

        new_position = [currentPosition[0] + x, currentPosition[1] + y]

        #verify if move is valid
        if 0 <= new_position[0] < len(Game.matrix) and 0 <= new_position[1] < len(Game.matrix[0]):

            #Si solo esta el jugador  o enemigo se pone un espacio vacio
            if Game.matrix[currentPosition[0]][currentPosition[1]] == Game.turn:
                Game.matrix[currentPosition[0]][currentPosition[1]] = "-"

            #pero si hay mas cosas en esa posicion, entonces solo debo remover al jugador/enemigo
            else:
                Game.matrix[currentPosition[0]][currentPosition[1]].remove(Game.turn)

                #Si solo queda una cosa entonces se elimina la lista y queda solo su unico elemento
                if len(Game.matrix[currentPosition[0]][currentPosition[1]]) == 1:
                    Game.matrix[currentPosition[0]][currentPosition[1]] = Game.matrix[currentPosition[0]][currentPosition[1]][0]
                #creo que tendré que hacer un elif de si queda vacío porque el len era 0, entonces toca cambiarlo por un "-"


            if Game.matrix[new_position[0]][new_position[1]] == "-":
                Game.matrix[new_position[0]][new_position[1]] = Game.turn
            
            elif type(Game.matrix[new_position[0]][new_position[1]]) == list:
                Game.matrix[new_position[0]][new_position[1]].append(Game.turn)
            
            else:
                Game.matrix[new_position[0]][new_position[1]] = [Game.matrix[new_position[0]][new_position[1]],Game.turn]


            Game.turn.position = new_position
            return True
        else:
            print(f"Movimiento {move} inválido")
            return False


    @staticmethod
    def switchTurn():
        if Game.turn == Game.player:
            Game.turn = Game.enemy
            
        else:
            Game.turn = Game.player
        
        print(f"Turno del {Game.turn.name} {Game.turn.icon}")

    @staticmethod    
    def verifyWinner():
        if Game.player.isDead():
            print(f"{Game.enemy.name},{Game.enemy.icon} ha ganado!")
            return True
        elif Game.enemy.isDead():
            print(f"{Game.player.name},{Game.player.icon} ha ganado!")
            return True
        else: 
            return False


    @staticmethod
    def setCharactersPosition(n):
        playerPosition = [random.randint(0,n-1),random.randint(0,n-1)]

        enemyPosition = [random.randint(0,n-1),random.randint(0,n-1)]

        while playerPosition == enemyPosition:
            enemyPosition = [random.randint(0,n-1),random.randint(0,n-1)]

        Game.player.position = playerPosition
        Game.enemy.position = enemyPosition

        Game.matrix[playerPosition[0]][playerPosition[1]] = Game.player
        Game.matrix[enemyPosition[0]][enemyPosition[1]] = Game.enemy

    @staticmethod
    def setItemsPosition(n):

        for i in range(n):
            for j in range(n):
                if Game.matrix[i][j] != "-":
                    continue
                putItem = random.randint(0,2)
                if putItem == 0:
                    continue
                typeItem = random.randint(0,1)

                if typeItem == 0:
                    item = random.choice(Game.food)
                else:
                    item = random.choice(Game.weapons)
                
                Game.matrix[i][j] = item


    @staticmethod
    def initMatrix(n):
        Game.matrix = [["-"for i in range(n)]for i in range(n)]
        
        Game.setCharactersPosition(n)

        Game.setItemsPosition(n)
        
        


        
        
        


    @staticmethod
    def startGame(n):
        print("Parpadea para seleccionar el tamaño del tablero. Cuando hayas seleccionado el tamaño sube la cabeza")
        while True:
            
            FaceDetection.detect(Game.cam)
            if FaceDetection.playerAction == "closed eyes":
                n += 1
                print("valor de n:",n)

            if FaceDetection.playerAction == "up":
                FaceDetection.playerAction = None
                break

            FaceDetection.playerAction = None
            time.sleep(0.3)
            

        Game.clearConsole()

        while(True):
            print("Nueva partida Iniciada")
            Game.player = Player()
            Game.enemy = Enemy()
            Game.initMatrix(n)
            Game.switchTurn()
            Game.play()

            #while(True)
            time.sleep(2)
            playAgain = Game.playAgain()
            
            if not playAgain:
                break


            #si se cumple cierta condición, continuar o finalizar el juego (podría hacerse tambien con un gesto)

    @staticmethod
    def playAgain():
        print("Sube las cejas para jugar de nuevo, de lo contrario, baja la cabeza")
        while True:
            FaceDetection.detect(Game.cam)
            if FaceDetection.playerAction == "eyebrows":
                FaceDetection.playerAction = None
                return True

            elif FaceDetection.playerAction == "down":
                return False

            FaceDetection.playerAction = None
            time.sleep(0.3)



