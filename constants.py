import pygame
# align sizes to a grid

windowWidth = int(400/15)*15 
windowHeight = int(400/15)*15 

borderWidth = 15 * 2 # thickness relative to center, so half of it will be outside of window..

snake_size = 15
apple_size = 15

margin = borderWidth / 2

FRAMERATELIMITER = 15
#colors rgb
SKYBLUE = (135,206,235)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#alias for directions
direction_UP = [0, -1]
direction_DOWN = [0, 1]
direction_LEFT = [-1, 0]
direction_RIGHT = [1, 0]

#font
pygame.font.init()
score_font = pygame.font.SysFont("comicsansms", 20)

# ML pysnake consts
DEATH_REWARD = -100
IDLE_REWARD = 0
APPLE_REWARD = 10

RESIZED_WIDTH = 80
RESIZED_HEIGHT = 80

#Hyperparams
num_actions = 4
scenes_toNet = 2
replayBufferCapacity = 1000
num_epochs = 100
MAX_STEPS = 500
BATCH_SIZE = 20
GAMMA = 0.99

headless = True