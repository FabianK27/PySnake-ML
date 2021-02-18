import pygame
import constants
from worldObject import *

#class snakePart(worldObject):
#    def __init__(self, disp, posX, posY, col, velX = 0 , velY = 0, sizeX = constants.snake_size, sizeY = constants.snake_size):
#         super(snakePart, self).__init__(disp, posX, posY, col, velX, velY, sizeX, sizeY)
        

        



class snake():
    def __init__(self, disp, posX, posY):
        #create head and add it to list of body parts
        self.head = worldObject(disp, posX, posY, constants.BLACK, velX = 0, velY = constants.snake_size, sizeX = constants.snake_size, sizeY = constants.snake_size)
        self.partList = [self.head]
        self.direction = constants.direction_LEFT
        self.head.setVelocity(self.head.getVelocityAbs() * self.direction[0], self.head.getVelocityAbs() * self.direction[1])
    def update(self):
        self.head.setVelocity(self.head.getVelocityAbs() * self.direction[0], self.head.getVelocityAbs() * self.direction[1])
        for part in self.partList:
            part.update()

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
