import pygame
import numpy as np
from worldObject import worldObject
import random
import constants

def randomPos(minNum, maxNum):
    return random.randint(minNum, maxNum)

def randomPosAligned(minNum, maxNum, gridSize):
    pos = int(random.randrange(minNum, maxNum) / gridSize) * gridSize
    if (pos + gridSize > maxNum):
        return pos - gridSize
    return pos


class apple(worldObject):
    def __init__(self, disp):
        super(apple, self).__init__(disp, randomPosAligned(constants.margin, constants.windowWidth - constants.margin, constants.snake_size), randomPosAligned(constants.margin, constants.windowHeight-constants.margin, constants.snake_size), 
                                    constants.RED, velX = 0, velY = 0, sizeX = constants.apple_size, sizeY = constants.apple_size)

    def onCollision(self):
        self.posX = randomPosAligned(constants.margin, constants.windowWidth - constants.margin, constants.snake_size)
        self.posY = randomPosAligned(constants.margin, constants.windowHeight - constants.margin, constants.snake_size)


        
        