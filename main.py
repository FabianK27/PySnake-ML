import pygame
from GameLoop import gameLoop
import constants



if __name__ == "__main__":
    print("ENTRY POINT")

    gLoop = gameLoop(constants.windowWidth, constants.windowHeight, "TEST")
    

"""
TODO:
- border collision
- text font for counter of success
- increasing snake length
- self collision 
"""