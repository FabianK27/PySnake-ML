import pygame
import constants
from worldObject import *

#class snakePart(worldObject):
#    def __init__(self, disp, posX, posY, col, velX = 0 , velY = 0, sizeX = constants.snake_size, sizeY = constants.snake_size):
#         super(snakePart, self).__init__(disp, posX, posY, col, velX, velY, sizeX, sizeY)
        

        



class snake():
    def __init__(self, disp, posX, posY):
        #create head and add it to list of body parts
        self.disp = disp
        self.head = worldObject(disp, posX, posY, constants.BLACK, velX = 0, velY = constants.snake_size, sizeX = constants.snake_size, sizeY = constants.snake_size)
        self.partList = [self.head]
        self.direction = constants.direction_LEFT
        self.head.setVelocity(self.head.getVelocityAbs() * self.direction[0], self.head.getVelocityAbs() * self.direction[1])

    def update(self, headOnly = False):
        self.head.setVelocity(self.head.getVelocityAbs() * self.direction[0], self.head.getVelocityAbs() * self.direction[1])
        if (headOnly):
            self.head.update()
            return
        for (i, part) in enumerate(self.partList[-1:0:-1]): #start at end, go until first(exclusive!) in reverse order
            part.setPosition(self.partList[-(i+2)].getPosition()[0], self.partList[-(i+2)].getPosition()[1])
            part.update()
        self.head.update()

    def changeDirection(self, newDirection):
        #check if change is compatible with current direction, if so then change
        if newDirection == constants.direction_UP and self.direction != constants.direction_DOWN:
            self.direction = newDirection
            return
        if newDirection == constants.direction_DOWN and self.direction != constants.direction_UP:
            self.direction = newDirection
            return
        if newDirection == constants.direction_LEFT and self.direction != constants.direction_RIGHT:
            self.direction = newDirection
            return
        if newDirection == constants.direction_RIGHT and self.direction != constants.direction_LEFT:
            self.direction = newDirection
            return

    def collideWithApple(self, apple_x, apple_y):
        if (self.head.posX == apple_x and self.head.posY == apple_y):
            return True
        return False

    def hasHitBorder(self):
        #note: in second cases we subtract borderWIdth = 2 * margin to adjust for snake head width / height
        if (self.head.posX < constants.margin or self.head.posX > constants.windowWidth - constants.borderWidth or self.head.posY < constants.margin or self.head.posY > constants.windowHeight - constants.borderWidth):
            return True
        return False

    def getLength(self):
        return len(self.partList)

    def grow(self):
        self.partList.append(worldObject(self.disp, self.head.posX, self.head.posY, constants.GREEN, constants.snake_size, constants.snake_size)) 
        #add new part where head currently is, we will then only update head in this iteration

    def hasSelfCollided(self):
        for part in self.partList[1::]:
            if (part.posX == self.head.posX and part.posY == self.head.posY):
                return True
        return False
