# 3rd party modules
import pygame


# game files
import constants


#############################################
# Structure
#############################################

class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path
# if tile is False player can walk over it.
# if tile is True player can NOT walk over it.


#############################################
# Objects
#############################################

class obj_Actor:
    """Our basic actor object."""

    def __init__(self, x, y, sprite):
        """Create the actor and set its coordinates."""
        self.x = x  # map address (not a pixel address)
        self.y = y  # map address (not a pixel address)
        self.sprite = sprite

    def draw(self):
        """Have the actor draw itself."""
        SURFACE_MAIN.blit(self.sprite, (self.x*constants.CELL_WIDTH,
                                        self.y*constants.CELL_HEIGHT))

    def move(self, dx, dy):
        """Move the actor.
        dx = distance to move x.  dy = distance to move y.
        The actor checks where it and where he wants to move to.
        Decides if where he wants to move to is a floor tile or a wall tile.
        """
        if GAME_MAP[self.x + dx][self.y + dy].block_path == False:
            self.x += dx
            self.y += dy


#############################################
# Map
#############################################

def map_create():
    new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]


    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    return new_map

#############################################
# Drawing
#############################################

def draw_game():
    """
    Game
    """

    global SURFACE_MAIN

    # clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(GAME_MAP)

    #draw the character
    PLAYER.draw()

    # update the display
    pygame.display.flip()

def draw_map(map_to_draw):

    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path == True: # if True there is a wall here
                #draw wall
                SURFACE_MAIN.blit(constants.S_WALL, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
            else:
                #draw floor
                SURFACE_MAIN.blit(constants.S_FLOOR, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))

def game_main_loop():
    """In this function we loop the main game."""
    game_quit = False

    while not game_quit:

        # get player input
        events_list = pygame.event.get()

        #process input
        for event in events_list:  # loop through all events that have happened
            if event.type == pygame.QUIT:  # QUIT attribute - someone closed window
                game_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    PLAYER.move(0, -1)
                if event.key == pygame.K_DOWN:
                    PLAYER.move(0, 1)
                if event.key == pygame.K_LEFT:
                    PLAYER.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    PLAYER.move(1, 0)
         #draw the game
        draw_game()

    pygame.quit()
    exit()

def game_initialize():
    """This function initializes the main window, and pygame"""

    global SURFACE_MAIN, GAME_MAP, PLAYER
    # initialize pygame
    pygame.init()

    # set sufrace dimensions
    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))
    # Ideally the surface should be resizable -- we are going to skip this for now

    GAME_MAP = map_create() # Create the game map. Fills the 2D array with values.

    PLAYER = obj_Actor(0, 0, constants.S_PLAYER)


if __name__ == '__main__':
    game_initialize()
    game_main_loop()
