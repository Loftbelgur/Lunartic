# 3rd party modules
import pygame
import random
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
# Components
#############################################

class com_Creature:

    """
    Creatures have health and can damage other objects by attacking them,
    can also die.
    """

    def __init__(self, name_instance, hp = 10):

        self.name_instance = name_instance
        self.hp = hp

#############################################
# AI
#############################################
class ai_Test:
    """
    Once per turn, exectue.
    """

    def take_turn(self):

        self.owner.move(random.randint(-1,1), random.randint(-1,1))

#############################################
# Objects
#############################################

class obj_Actor:
    """Our basic actor object."""

    def __init__(self, x, y, name_object, sprite, creature = None, ai = None):
        """Create the actor and set its coordinates."""
        self.x = x  # map address (not a pixel address)
        self.y = y  # map address (not a pixel address)
        self.sprite = sprite

        self.creature = creature
        if creature:
            self.creature = creature
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

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

class obj_Spritesheet:
    """
    Class used to grab images out of a sprite sheet
    """

    def __init__(self, file_name):
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.tiledict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5,
                        'f': 6, 'g': 7, 'h': 8,'i': 9,'j' :10,'k': 11,'l': 12
                        ,'m': 13,'n': 14,'o': 15,'p': 16}

    def get_image(self, column, row, width = constants.CELL_WIDTH,
                    height = constants.CELL_HEIGHT, scale = None):

        """ Scale is a tuple, returns a single image """
        image = pygame.Surface([width, height]).convert()

        # Blit the image to assigned location, last two rows are the image adress in sprite sheet

        image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column]*width, row*height, width, height))


        image.set_colorkey(constants.COLOR_BLACK)

        # Scaling the images if we need to scale it

        if scale:
            (new_w, new_h) = scale

            image = pygame.transform.scale(image, (new_w, new_h))

        return image

#############################################h
# Map
#############################################

def map_create():
    new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    new_map[0][0].block_path = True
    new_map[0][1].block_path = True
    new_map[0][2].block_path = True
    new_map[0][3].block_path = True
    new_map[0][4].block_path = True
    new_map[0][5].block_path = True
    new_map[0][6].block_path = True
    new_map[0][7].block_path = True
    new_map[0][8].block_path = True
    new_map[0][9].block_path = True
    new_map[0][10].block_path = True
    new_map[0][11].block_path = True

    new_map[1][0].block_path = True
    new_map[2][0].block_path = True
    new_map[3][0].block_path = True

    new_map[5][5].block_path = True

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
    for obj in GAME_OBJECTS:
        obj.draw()

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

    # player action definition
    # Want to tell the game when player take action and when it can take an action
    player_action = "no-action"

    while not game_quit:

        #handle player input
        player_action = game_handle_keys()

        if player_action == "QUIT":
            game_quit = True

        if player_action != "no-action":
            for obj in GAME_OBJECTS:
                if obj.ai:
                    obj.ai.take_turn()

        # draw game
        draw_game()

    pygame.quit()
    exit()

def game_handle_keys():

    # get player input
    events_list = pygame.event.get()

    #process input
    for event in events_list:  # loop through all events that have happened
        if event.type == pygame.QUIT:  # QUIT attribute - someone closed window
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.move(0, -1)
                return "player-moved"
            if event.key == pygame.K_DOWN:
                PLAYER.move(0, 1)
                return "player-moved"
            if event.key == pygame.K_LEFT:
                PLAYER.move(-1, 0)
                return "player-moved"
            if event.key == pygame.K_RIGHT:
                PLAYER.move(1, 0)
                return "player-moved"
    return "no-action"

def game_initialize():
    """This function initializes the main window, and pygame"""

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS
    # initialize pygame
    pygame.init()

    # set sufrace dimensions
    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))
    # Ideally the surface should be resizable -- we are going to skip this for now

    GAME_MAP = map_create() # Create the game map. Fills the 2D array with values.


    # TEMPORARY SPRITES ""

    spritesheet = obj_Spritesheet('data/char.png')

    # Column, row, sprite size m / n , scale size
    S_PLAYER = spritesheet.get_image('b', 4, 32, 32, (32, 32))

    creature_com1 = com_Creature('siggi')
    PLAYER = obj_Actor(1, 1, 'human' ,S_PLAYER, creature = creature_com1)

    creature_com2 = com_Creature('jon')
    ai_com = ai_Test()
    ENEMY = obj_Actor(12,12, 'alien', constants.S_ENEMY, ai = ai_com)

    ai_com1 = ai_Test()
    ENEMY2 = obj_Actor(10,10, 'alien2', constants.S_ENEMY, ai = ai_com1)

    GAME_OBJECTS = [PLAYER, ENEMY, ENEMY2]

if __name__ == '__main__':
    game_initialize()
    game_main_loop()
