import pygame
from GameLoop import gameLoop
import constants
from pySnakeML import gameLoopML
import time
from models import randomNN


if __name__ == "__main__":
    print("ENTRY POINT")
    randomAgent = randomNN(4)
    #gLoop = gameLoop(constants.windowWidth, constants.windowHeight, "TEST")
    gLoop = gameLoopML(constants.windowWidth, constants.windowHeight, "TEST")
    while(gLoop.isOpen):
        gameOver, reward = gLoop.step(randomAgent.returnAction())
        #time.sleep(0.3)

    print(reward)