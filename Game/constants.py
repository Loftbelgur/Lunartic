import pygame

pygame.init()

#############################################
# Window and map size
#############################################

# Game sizes
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

# MAP VARS
MAP_WIDTH = 30
MAP_HEIGHT = 30

#############################################
# Colors
#############################################

# Color definitions
COLOR_BLACK = (0, 0, 0)  # RGB for black
COLOR_WHITE = (255, 255, 255)  # RGB for white
COLOR_GREY = (100, 100, 100) # RGB for grey
COLOR_RED = (255, 0, 0) # RGB for red
COLOR_GREEN = (0, 128, 0) # RGB for green

# Game colors
COLOR_DEFAULT_BG = COLOR_GREY

#############################################
# Sprites
#############################################

# TO do : Make LUnartic constant for paths.
# character
S_PLAYER = pygame.image.load('data/python.png')
S_ENEMY = pygame.image.load('data/crab.png')
S_WALL = pygame.image.load('data/wall.png')
S_FLOOR = pygame.image.load('data/floor.jpg')
