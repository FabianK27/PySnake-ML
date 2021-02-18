import constants
import pygame
import numpy as np

class worldObject:
    """ abstract class that provides methods for world Objects"""
    def __init__(self, disp, posX, posY, col, sizeX, sizeY, velX=0, velY=0):
        self.col = col
        self.disp = disp
        self.posX = posX
        self.posY = posY
        self.velX = velX
        self.velY = velY
        self.sizeX = sizeX
        self.sizeY = sizeY

        pygame.draw.rect(disp, col, [posX, posY, sizeX, sizeY])

    def getPosition(self):
        return [self.posX, self.posY]
    def setPosition(self, x, y):
        self.posX = x
        self.posY = y

    def getVelocity(self):
        return [self.velX, self.velY]
    def setVelocity(self, v_x, v_y):
        self.velX, self.velY = v_x, v_y
    def getVelocityAbs(self):
        return np.sqrt(self.velX*self.velX + self.velY * self.velY)

    def update(self):
        self.posX += self.velX
        self.posY += self.velY
        pygame.draw.rect(self.disp, self.col, [self.posX, self.posY, self.sizeX, self.sizeY])

    def boundingBox(self):
        return [self.posX, self.posY, self.posX + self.sizeX, self.posY + self.sizeY]

    def collisionWith(self, obj2):
        pass


    