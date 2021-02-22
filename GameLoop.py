import pygame
from Board import board
import constants
from Snake import *
from Apple import apple

class gameLoop:
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



        self.run()


    def run(self):


        self.isOpen = True
        while self.isOpen:
            self.eventManager()
            self.update()

        #game over
        ## could print a gameover screen but for ML we dont want it
        print("End Score: " + str(len(self.snake.partList) - 3))
            
        pygame.quit()
        quit()




    def eventManager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.snake.changeDirection(constants.direction_UP)
                continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.snake.changeDirection(constants.direction_DOWN)
                continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.snake.changeDirection(constants.direction_LEFT)
                continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.snake.changeDirection(constants.direction_RIGHT)
                continue  
        if self.snake.collideWithApple(self.apple.posX, self.apple.posY):
            print("COLLISION")
            self.apple.onCollision()
            self.foodEaten = True
            self.snake.grow()


    def update(self):
        if(self.checkBorderCollision()):
            return


        self.board.update()

        self.snake.update(headOnly=self.foodEaten)
        if(self.checkSelfCollision()):
            return

        self.foodEaten = False
        self.apple.update()

        self.displayScore(self.snake.getLength() - 3)
        pygame.display.update()
        self.clock.tick(constants.FRAMERATELIMITER)

    def checkBorderCollision(self):
        if(self.snake.hasHitBorder()):
            print("BORDER COLLISION!")
            self.isOpen = False
            return True
    def checkSelfCollision(self):
        if(self.snake.hasSelfCollided()):
            print("SELF COLLISION")
            self.isOpen = False
            return True

    def displayScore(self, score):
        self.disp.blit(constants.score_font.render("Score: " + str(score), True, constants.YELLOW), [constants.margin, constants.margin])

    def gameOverScreen(self):
        self.disp.blit(constants.score_font.render("GAME OVER!", True, constants.YELLOW), [constants.windowWidth/2, constants.windowHeight/2])
        self.disp.blit(constants.score_font.render("Score: " + str(len(self.snake.partList)-3), True, constants.YELLOW), [constants.windowWidth/2 + constants.borderWidth, constants.windowHeight/2 + constants.borderWidth])