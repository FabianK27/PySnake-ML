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



        self.run()


    def run(self):
        self.isOpen = True
        while self.isOpen:
            self.eventManager()
            self.update()
            
        pygame.quit()
        quit()




    def eventManager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isOpen = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.isOpen = False
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

    def update(self):

        self.board.update()
        self.snake.update()
        self.apple.update()
        pygame.display.update()
        self.clock.tick(constants.FRAMERATELIMITER)