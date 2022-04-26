import os, sys
from os import error

class InvalidMove(error):
    pass

class Snake:
    length=3
    previousTail = [0,0]
    def __init__(self, snakelist, tag):
        self.tag = tag
        self.head= snakelist[0]
        self.body= []
        self.body.append(snakelist[1])
        self.body.append(snakelist[2])
        if self.head[0]==self.body[0][0]:
            if self.head[1] > self.body[0][1]:
                self.lastDirection=1 # headed right
            else:
                self.lastDirection=3 # headed left
        else:
            if self.head[0] < self.body[0][0]:
                self.lastDirection = 0 #headed up
            else:
                self.lastDirection = 2 #headed down
 
    def printHead(self):
        outFile.write('\n',self.head)

    def printBody(self):
        for elem in self.body:
            outFile.write('\n',elem)    

    def __moveBodyToHead(self):
        self.previousTail = self.body[self.length-2]
        for i in range(self.length-2, 0, -1):
            self.body[i] = self.body[i-1]
        x,y = self.head
        self.body[0]= [x,y] # same bs

    #functie mutare cerinta 4
    def move(self, direction, foodList):
        if direction<0 or direction>3:
            raise InvalidMove("Direction must be between 0 and 3")
        if (direction + 2)%4 == self.lastDirection:
            raise InvalidMove("The snake can't move over its own body")
        else:
            if direction == 0:
                if self.head[0] > 0:    
                    self.__moveBodyToHead()
                    self.head[0] -= 1
                else:
                    raise InvalidMove("Out of the map")
            elif direction == 1:
                if self.head[1] < W-1:
                    self.__moveBodyToHead()
                    self.head[1] += 1
                else:
                    raise InvalidMove("Out of the map")
            elif direction == 2:
                if self.head[0] < H-1:    
                    self.__moveBodyToHead()
                    self.head[0] += 1
                else:
                    raise InvalidMove("Out of the map")
            elif direction == 3:
                if self.head[1] > 0:    
                    self.__moveBodyToHead()
                    self.head[1] -= 1
                else:
                    raise InvalidMove("Out of the map")
            if self.head in foodList: # 
                x,y = self.previousTail
                self.body.append([x,y])
                self.length+=1
                x,y = self.head
                foodList.remove([x,y])
                outFile.write("\nSarpele "+ self.tag+ " a mancat bobul de la linia "+str(x)+" coloana "+str(y))
                return 1#cost
        if direction == self.lastDirection:
            return 2 #cost
        else:
            self.lastDirection = direction
            return 3 #cost
            

class Game:
    totalCost=0
    printCount=1
    def __init__ (self, graf, size):
        self.graf = graf
        self.snakeSizeFinal = size
        self.food = self.__getFood()
        snakes = self.__getSnakes()
        self.snakeA = Snake(snakelist=snakes[0], tag='a')
        self.snakeB = Snake(snakelist=snakes[1], tag='b')
        self.snakeC = Snake(snakelist=snakes[2], tag='c')
        self.snakeD = Snake(snakelist=snakes[3], tag='d')
        self.snakeList = [self.snakeA, self.snakeB, self.snakeC, self.snakeD]

    def printMap(self): #prints the game map to the output file
        outFile.write('\n'+str(self.printCount))
        for linie in self.graf:
            outFile.write('\n')
            for elem in linie:
                outFile.write(elem+ ' ')
        outFile.write('\n')
        self.printCount+=1
    
    def __getFood(self): #gets the food coordinates in a list
        food=[]
        for i in range(len(self.graf)):
            for j in range(len(self.graf[0])):
                if graf[i][j]=='*':
                    food.append([i,j])
        return food

    def __getSnakes(self): #method for getting the snakes in a list of lists, from head to tail
        snakes=[ [[],[],[]],
                 [[],[],[]],
                 [[],[],[]],
                 [[],[],[]] ]
        
        for i in range(len(self.graf)):
            for j in range(len(self.graf[0])):
                if graf[i][j]=='A':
                    snakes[0][0]=[i,j]
                elif graf[i][j]=='B':
                    snakes[1][0]=[i,j]
                elif graf[i][j]=='C':
                    snakes[2][0]=[i,j]
                elif graf[i][j]=='D':
                    snakes[3][0]=[i,j]

                elif graf[i][j]=='a':
                    if graf[i+1][j] == 'A' or graf[i-1][j] == 'A' or graf[i][j+1] == 'A' or graf[i][j-1] == 'A':
                        snakes[0][1]=[i,j]
                    else:
                        snakes[0][2]=[i,j]
                
                elif graf[i][j]=='b':
                    if graf[i+1][j] == 'B' or graf[i-1][j] == 'B' or graf[i][j+1] == 'B' or graf[i][j-1] == 'B':
                        snakes[1][1]=[i,j]
                    else:
                        snakes[1][2]=[i,j]
                
                elif graf[i][j]=='c':
                    if graf[i+1][j] == 'C' or graf[i-1][j] == 'C' or graf[i][j+1] == 'C' or graf[i][j-1] == 'C':
                        snakes[2][1]=[i,j]
                    else:
                        snakes[2][2]=[i,j]
                
                elif graf[i][j]=='d':
                    if graf[i+1][j] == 'D' or graf[i-1][j] == 'D' or graf[i][j+1] == 'D' or graf[i][j-1] == 'D':
                        snakes[3][1]=[i,j]
                    else:
                        snakes[3][2]=[i,j]
        return snakes

    #cerinta10
    def __updateMap(self): #method to change the map according to the new snake positions
        for snake in self.snakeList:
            line, col = snake.head
            self.graf[line][col] = snake.tag.upper()
            line, col = snake.previousTail
            self.graf[line][col] = '.'
            for elem in snake.body:
                line,col = elem
                self.graf[line][col] = snake.tag

    def __checkSquare(self, line, col): #auxiliary method to check if there is a square on the map
        for j in range(self.snakeSizeFinal+1):
            if not self.graf[line][j+col].isalpha():
                return 0
            if not self.graf[line+self.snakeSizeFinal][j+col].isalpha():
                return 0

        for i in range(self.snakeSizeFinal+1):
            if not self.graf[i+line][col].isalpha():
                return 0
            if not self.graf[i+line][col+self.snakeSizeFinal].isalpha():
                return 0
        
        return 1

    #cerinta 3
    def moveSnakes(self, directionA, directionB, directionC, directionD): #moves the snake in the specified positions
        roundTotal=0
        roundTotal += self.snakeA.move(directionA, self.food)
        roundTotal += self.snakeB.move(directionB, self.food)
        roundTotal += self.snakeC.move(directionC, self.food)
        roundTotal += self.snakeD.move(directionD, self.food)
        self.__updateMap()
        self.totalCost+=roundTotal
        return roundTotal

    #cerinta5
    def checkWin(self): #checks for the win condition
        if self.snakeA.length == self.snakeB.length == self.snakeC.length == self.snakeD.length == self.snakeSizeFinal:
            for line in range(len(self.graf)):
                for col in range(len(self.graf[line])):
                    if self.graf[line][col].isalpha():
                        return self.__checkSquare(line, col)
        else:
            return 0
            


if __name__ == "__main__":

    folderIN, folderOUT, NSOL, timeout = sys.argv[1:] #cerinta1

    fisiereIN=os.listdir(folderIN)

    if not os.path.exists(folderOUT):
        os.mkdir(folderOUT)
    for numeFisier in fisiereIN:
        numeFisier=numeFisier[:-3]
        numeFisierOutput="output_"+numeFisier+".out"
        print(numeFisier, "--->", numeFisierOutput)
        f=open("folder_output/"+numeFisierOutput,"w")
        f.close()

    fisiereOUT = os.listdir(folderOUT)

    fileIndex=0 #setare fisier
 
    inFile = open(folderIN+'/'+fisiereIN[fileIndex], 'r') #cerinta2
    outFile = open(folderOUT+'/'+fisiereOUT[fileIndex], 'w')
    snakeSizeFinal = int(inFile.readline())
    graf=[]
    lines = inFile.readlines()
    for line in lines:
        graf.append(list(line.replace('\n','')))
    H = len(graf)
    W = len(graf[0])
    if snakeSizeFinal > min(H,W):
        print("jocul nu se poate castiga")

    game = Game(graf, snakeSizeFinal)
    print('Win=',game.checkWin())
    game.printMap()
    cost = game.moveSnakes(0,1,2,3)
    print(cost)
    game.printMap()
    game.moveSnakes(3, 0, 3, 2)
    game.printMap()
    print('Win=',game.checkWin())