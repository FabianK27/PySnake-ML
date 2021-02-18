# align sizes to a grid

windowWidth = int(800/15)*15 
windowHeight = int(600/15)*15 

borderWidth = 15 * 2 # thickness relative to center, so half of it will be outside of window..

snake_size = 15
apple_size = 15

margin = borderWidth / 2

FRAMERATELIMITER = 10
#colors rgb
SKYBLUE = (135,206,235)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#alias for directions
direction_UP = [0, -1]
direction_DOWN = [0, 1]
direction_LEFT = [-1, 0]
direction_RIGHT = [1, 0]