import pygame
from GameLoop import gameLoop
import constants
from pySnakeML import gameLoopML
import time
from models import randomNN


if __name__ == "__main__":
    print("ENTRY POINT")
    randomAgent = randomNN(4)
    for i in range(10):
        gLoop = gameLoopML(constants.windowWidth, constants.windowHeight, "TEST " + str(i))
        while(gLoop.isOpen):
            gameOver, reward = gLoop.step(randomAgent.returnAction())
            print(reward)
            time.sleep(0.1)
        time.sleep(3)
        del gLoop

    