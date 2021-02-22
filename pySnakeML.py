import pygame
from Board import board
import constants
from Snake import *
from Apple import apple
from GameLoop import *
import PIL
import numpy as np
import torch

debug = False

class gameLoopML:
    """Main loop that sets up and runs screen"""
    def __init__(self, windowWidth, windowHeight, title):
        pygame.init()
        self.disp = pygame.display.set_mode((windowWidth, windowHeight))
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        pygame.display.set_caption(title)
        #setup a board
        self.board = board(self.disp)
        #create a snake
        self.snake = snake(self.disp, ((windowWidth / 2) // constants.snake_size)*constants.snake_size, ((windowHeight / 2) // constants.snake_size)*constants.snake_size)
        #create a clock to manage fps
        self.clock = pygame.time.Clock()
        #create an apple
        self.apple = apple(self.disp)

        self.foodEaten = False

        self.isOpen = True


        #create userevents for movement
        self.inputUP = pygame.event.Event(pygame.USEREVENT +1)
        self.inputDOWN = pygame.event.Event(pygame.USEREVENT +2)
        self.inputLEFT = pygame.event.Event(pygame.USEREVENT + 3)
        self.inputRIGHT = pygame.event.Event(pygame.USEREVENT + 4)

        self.step(2) # first event fixed for now
        
        

        


    def step(self, input): # input in [0,1,2,3] mapped to key UP, DOWN, LEFT, RIGHT
        self.mapIntToInput(input) # trigger appropriate event
        self.eventManager() # execute event
        self.update() # update game
        if debug:
            print("step completed")
        
        #return gameOver bool and reward

        return [not self.isOpen, self.reward()] # for convenience we interpret return value as gameOver so return not isOpen



    def eventManager(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.type == pygame.USEREVENT + 1:
                if debug:
                    print("UP")
                self.snake.changeDirection(constants.direction_UP)
                continue
            if event.type == pygame.USEREVENT + 2:
                if debug:
                    print("DOWN")
                self.snake.changeDirection(constants.direction_DOWN)
                continue
            if event.type == pygame.USEREVENT + 3:
                if debug:
                    print("LEFT")
                self.snake.changeDirection(constants.direction_LEFT)
                continue
            if event.type == pygame.USEREVENT + 4:
                if debug:
                    print("RIGHT")
                self.snake.changeDirection(constants.direction_RIGHT)
                continue  

        if self.snake.collideWithApple(self.apple.posX, self.apple.posY):
            if debug:
                print("COLLISION")
            self.apple.onCollision() # if snake gets large sometimes apple can spawn in snake's body. Maybe thats bad...
            self.foodEaten = True
            self.snake.grow()


    def update(self):

        self.board.update()

        self.snake.update(headOnly=self.foodEaten)
        if(self.checkSelfCollision()):
            pygame.display.update()
            return
        if(self.checkBorderCollision()):
            pygame.display.update()
            return

        #self.foodEaten = False
        self.apple.update()
 
       # self.displayScore(self.snake.getLength() - 3) #dont want that in ml images
        pygame.display.update()
        

    def checkBorderCollision(self):
        if(self.snake.hasHitBorder()):
            if debug:
                print("BORDER COLLISION!")
            self.isOpen = False
            return True
    def checkSelfCollision(self):
        if(self.snake.hasSelfCollided()):
            if debug:
                print("SELF COLLISION")
            self.isOpen = False
            return True

    def displayScore(self, score):
        self.disp.blit(constants.score_font.render("Score: " + str(score), True, constants.YELLOW), [constants.margin, constants.margin])

    def gameOverScreen(self):
        self.disp.blit(constants.score_font.render("GAME OVER!", True, constants.YELLOW), [constants.windowWidth/2, constants.windowHeight/2])
        self.disp.blit(constants.score_font.render("Score: " + str(len(self.snake.partList)-3), True, constants.YELLOW), [constants.windowWidth/2 + constants.borderWidth, constants.windowHeight/2 + constants.borderWidth])

    def mapIntToInput(self, intInput):
        pygame.event.clear()
        if (intInput == 0):
            pygame.event.post(self.inputUP)
        elif (intInput == 1):
            pygame.event.post(self.inputDOWN)
        elif (intInput == 2):
            pygame.event.post(self.inputLEFT)
        elif (intInput == 3):
            pygame.event.post(self.inputRIGHT)
        else:
            print("UNKNOWN INPUT RECEIVED")

    def reward(self):
        if(self.foodEaten):
            self.foodEaten = False
            return constants.APPLE_REWARD
        if(not self.isOpen):
            return constants.DEATH_REWARD
        return constants.IDLE_REWARD

    def get_screen(self, color = False):
        """return the current screen as an array of width x height, either rgb or greyscale"""
        imgString = pygame.image.tostring(self.disp, 'RGB')
        img = PIL.Image.frombytes('RGB', (constants.windowWidth, constants.windowHeight), imgString)
        if (not color):
            img = img.convert('L') # convert to greyscale
        img = img.resize((constants.RESIZED_WIDTH, constants.RESIZED_HEIGHT))
        #if (not color):
         #   img = img.convert('1') # convert to bi-level image, ??
         #   img.save("test.png", "PNG")
        matrix = np.asarray(img.getdata(), dtype=np.float64) / 255 #normalize
        matrix = matrix.reshape(1, img.size[1], img.size[0])
        return torch.from_numpy(matrix).unsqueeze(0) # return as torch.tensor with shape (B,C,H,W)