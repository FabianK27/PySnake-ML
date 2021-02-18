import pygame
import constants

class board:
    def __init__(self, disp):
        self.disp = disp
        
    def update(self):
        self.disp.fill(constants.SKYBLUE)
        #draw boarder rectangle 
        pygame.draw.rect(self.disp, constants.BLACK, [0, 0, constants.windowWidth, constants.windowHeight], width = constants.borderWidth)
