# 3rd party modules and python libraries
import pygame
import random
import itertools as it

# game files
import constants


#############################################
# Structure
#############################################
class struc_Tile:

    # if tile is False player can walk over it.
    # if tile is True player can NOT walk over it.
    def __init__(self, block_path):
        self.block_path = block_path

class struc_Assets:
    def __init__(self):

        # Spritesheet
        self.playerspritesheet = obj_Spritesheet('data/char.png')
        self.charspritesheet = obj_Spritesheet('data/alien.png')

        # Sprites ( Column, row, sprite size m / n , scale size )
        self.S_PLAYER = self.playerspritesheet.get_image('b', 4, 32, 32, (32, 32))
        self.S_ENEMY = self.charspritesheet.get_image('g', 8, 32, 32, (32, 32))
        self.S_ENEMY2 = self.charspritesheet.get_image('g', 12, 32, 32, (32, 32))

        self.S_WALL = self.charspritesheet.get_image('i', 0, 32, 32, (32, 32))
        self.S_FLOOR = self.charspritesheet.get_image('k', 4, 32, 32, (32, 32))

        # Fonts (Font file, size of font)
        self.FONT_DEBUG_MESSAGE = pygame.font.Font('data/joystix.ttf', 20)
        self.FONT_MESSAGE_TEXT = pygame.font.Font('data/joystix.ttf', 20)

#############################################
# Components
#############################################
class com_Creature:

    # Creatures have health and can damage other objects by attacking them,
    # can also die.
    def __init__(self, name_instance, hp = 10, death_function = None):

        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function

    # Move the actor. dx = distance to move x.  dy = distance to move y.
    def move(self, dx, dy):

        # The actor checks where it and where he wants to move to.
        tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)

        # Checks if creatures are in x or y direction, also checks self
        # since we don't want creatures to hurt themself if they don't move.
        target = map_check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            self.attack(target, 5)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    # Allows creatures to dealdamage.
    def attack(self, target, damage):
            game_message(self.name_instance + " attacks " +
            target.creature.name_instance + " for " +
            str(damage) + " damage!", constants.COLOR_WHITE)

            target.creature.take_damage(damage)

    # Allows creatures to take damage.
    def take_damage(self, damage):
        self.hp -= damage
        game_message(self.name_instance + "'s health is " +
                    str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)

        # Checks if creature hp is 0 or lower.
        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

#############################################
# AI
#############################################
class ai_Test:

    # Once per turn, exectue.
    def take_turn(self):

        self.owner.creature.move(random.randint(-1,1), random.randint(-1,1))

def death_monster(monster):

    # On death, makes monsters stop moving
    game_message(monster.creature.name_instance + " is dead!",
                constants.COLOR_GREY)

    # Turns off creature component and ai
    monster.creature = None
    monster.ai = None

#############################################
# Objects
#############################################
class obj_Actor:

    # Our basic actor object.
    def __init__(self, x, y, name_object, sprite, creature = None, ai = None):
        # Create the actor and set its coordinates.
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

        # Function to have the actor draw itself.
        SURFACE_MAIN.blit(self.sprite, (self.x*constants.CELL_WIDTH,
                                        self.y*constants.CELL_HEIGHT))

class obj_Game:

    # Swapping out global variables for objects.
    def __init__(self):

        self.current_map = map_create()
        self.current_objects = []
        self.message_history = []

    def transition_next(self):

        self.current_map = map_create2()
        self.current_objects = [PLAYER, ENEMY2]

#############################################
# Sprites
#############################################
class obj_Spritesheet:

    # Class used to grab images out of a sprite sheet
    def __init__(self, file_name):
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.tiledict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5,
                        'f': 6, 'g': 7, 'h': 8,'i': 9,'j' :10,'k': 11,'l': 12
                        ,'m': 13,'n': 14,'o': 15,'p': 16}

    def get_image(self, column, row, width = constants.CELL_WIDTH,
                    height = constants.CELL_HEIGHT, scale = None):

        # Scale is a tuple, returns a single image
        image = pygame.Surface([width, height]).convert()

        # Blit the image to assigned location, last two rows are the image adress in sprite sheet
        image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column]*width,
                    row*height, width, height))
        image.set_colorkey(constants.COLOR_BLACK)

        # Scaling the images if we need to scale it
        if scale:
            (new_w, new_h) = scale

            image = pygame.transform.scale(image, (new_w, new_h))

        return image

#############################################h
# Map
#############################################
# Did not get the map editor to work properly, had to hardcore the map
# Needs a fix, this is not proper coding... temp fix with itertools.
def map_create():
    new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    # map borders x direction
    for x in range(constants.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][constants.MAP_HEIGHT-1].block_path = True

    # map borders y direction
    for y in range(constants.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[constants.MAP_WIDTH-1][y].block_path = True

    for x in range(11, 18):
        new_map[x][6].block_path = True
        new_map[x][constants.MAP_HEIGHT-1].block_path = True

    for x in range(11, 18):
        new_map[x][3].block_path = True
        new_map[x][constants.MAP_HEIGHT-1].block_path = True

    for x in it.chain(range(1, 21), range(23, constants.MAP_HEIGHT)):
        new_map[x][9].block_path = True
        new_map[x][constants.MAP_HEIGHT-1].block_path = True

    for x in it.chain(range(1, 4), range(7, 13),
                        range(16, constants.MAP_HEIGHT)):

        new_map[x][18].block_path = True
        new_map[x][constants.MAP_HEIGHT-1].block_path = True

    for y in it.chain(range(1, 4), range(6, 9),
                    range(19, constants.MAP_HEIGHT)):

        new_map[10][y].block_path = True
        new_map[constants.MAP_WIDTH-1][y].block_path = True

    for y in it.chain(range(1, 4), range(6, 12), range(15, 21),
                        range(23, constants.MAP_HEIGHT)):

        new_map[18][y].block_path = True
        new_map[constants.MAP_WIDTH-1][y].block_path = True

    return new_map

def map_create2():
        new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

        # map borders x direction
        for x in range(constants.MAP_WIDTH):
            new_map[x][0].block_path = True
            new_map[x][constants.MAP_HEIGHT-1].block_path = True

        # map borders y direction
        for y in range(constants.MAP_HEIGHT):
            new_map[0][y].block_path = True
            new_map[constants.MAP_WIDTH-1][y].block_path = True

        return new_map

def map_check_for_creature(x, y, exclude_object = None):

    target = None

    # check objectlist to find creature at that location that isn't excluded.
    if exclude_object:
        for object in GAME.current_objects:
            if (object is not exclude_object and
                object.x == x and
                object.y == y and
                object.creature):

                target = object

            if target:
                return target
    else:
    # check objectlist to find any creature at that location.
        for object in GAME.current_objects:
            if (object.x == x and
                object.y == y and
                object.creature):

                target = object

            if target:
                return target

#############################################
# Drawing
#############################################
def draw_game():

    global SURFACE_MAIN

    # clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(GAME.current_map)

    #draw the character
    for obj in GAME.current_objects:
        obj.draw()

    draw_debug()
    draw_messages()
    # update the display
    pygame.display.flip()

def draw_map(map_to_draw):

    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path == True: # if True there is a wall here
                #draw wall
                SURFACE_MAIN.blit(ASSETS.S_WALL, (
                    x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
            else:
                #draw floor
                SURFACE_MAIN.blit(ASSETS.S_FLOOR, (
                    x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))

def draw_debug():

    # Tracks fps
    draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())),
                (0, 0), constants.COLOR_WHITE, constants.COLOR_BLACK)

def draw_messages():

    # Draws the items on the list. Negative to draw last messages
    if len(GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = GAME.message_history
    else:
        to_draw = GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = helper_text_height(ASSETS.FONT_MESSAGE_TEXT)

    # Equal to the height of the window, minus number of messages times text height
    start_y = constants.MAP_HEIGHT*constants.CELL_HEIGHT- (constants.NUM_MESSAGES * text_height) - 5

    i = 0
    for message, color in to_draw:

        draw_text(SURFACE_MAIN, message, (0, start_y + (i * text_height)),
                    color, constants.COLOR_BLACK)

        i += 1

# Takes in text and displays on the refrenced surface
def draw_text(display_surface, text_to_display,
                T_coords, text_color, back_color = None):

    # Get both the surface and rectangle of the desired message
    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)

    # adjust the location of the surface based on the coordinates
    text_rect.topleft = T_coords

    # draw the text onto the display surface
    display_surface.blit(text_surf, text_rect)

#############################################
# Helpers
#############################################
def helper_text_objects(incoming_text, incoming_color, incoming_bg):
    # Text rendering in pygame works by rendering from a font.
    # ( text, anti aliasing, color)
    # If statement adds an option so we can add a backround to our text.
    if incoming_bg:
        Text_surface = ASSETS.FONT_DEBUG_MESSAGE.render(
                incoming_text, False,
                incoming_color, incoming_bg)
    else:
        Text_surface = ASSETS.FONT_DEBUG_MESSAGE.render(
                incoming_text, False,
                incoming_color)

    return Text_surface, Text_surface.get_rect()

def helper_text_height(font):
    # Pass in a font, returns the height in pixels of the font.
    # Allows to change fonts without hardcoding. ( text, anti aliasing, color)
    font_object = font.render('a', False, (0, 0, 0))
    font_rect = font_object.get_rect()

    return font_rect.height

#############################################
# Game
#############################################
def game_main_loop():
    # In this function we loop the main game.
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
            for obj in GAME.current_objects:
                if obj.ai:
                    obj.ai.take_turn()

        # draw game
        draw_game()

        CLOCK.tick(constants.GAME_FPS)
    pygame.quit()
    exit()

def game_handle_keys():

    # get player input
    events_list = pygame.event.get()

    #process input
    for event in events_list:  # loop through all events that have happened
        if event.type == pygame.QUIT:  # QUIT attribute - someone closed window
            return "QUIT"

        # Directions for arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0, -1)
                return "player-moved"
            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                return "player-moved"
            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                return "player-moved"
            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                return "player-moved"

            # Swap maps ( ideal would be bound to a surface object)
            if event.key == pygame.K_h:
                GAME.transition_next()

    return "no-action"

def game_message(game_msg, msg_color):

    GAME.message_history.append((game_msg, msg_color))


def game_initialize():
    # This function initializes the main window, and pygame
    global SURFACE_MAIN, GAME, ASSETS, CLOCK, PLAYER, ENEMY, ENEMY2

    # initialize pygame
    pygame.init()

    # set surface dimensions
    SURFACE_MAIN = pygame.display.set_mode((
                                constants.MAP_WIDTH*constants.CELL_WIDTH,
                                constants.MAP_HEIGHT*constants.CELL_HEIGHT))

    GAME = obj_Game()

    ASSETS = struc_Assets()

    CLOCK = pygame.time.Clock()

    creature_com1 = com_Creature('Player')
    PLAYER = obj_Actor(1, 1, 'human' ,ASSETS.S_PLAYER, creature = creature_com1)

    creature_com2 = com_Creature('Alien', death_function = death_monster)
    ai_com = ai_Test()
    ENEMY = obj_Actor(24,24, 'alien', ASSETS.S_ENEMY,
                        creature = creature_com2, ai = ai_com)

    creature_com3 = com_Creature('Alien', death_function = death_monster)
    ai_com1 = ai_Test()
    ENEMY1 = obj_Actor(12, 12, 'alien', ASSETS.S_ENEMY,
                        creature = creature_com3, ai = ai_com1)

    ai_com2 = ai_Test()
    creature_com4 = com_Creature('Alien', death_function = death_monster)
    ENEMY2 = obj_Actor(5,5, 'alien', ASSETS.S_ENEMY,
                        creature = creature_com4, ai = ai_com2)

    creature_com3 = com_Creature('Alien Ghost', death_function = death_monster)
    ai_com3 = ai_Test()
    ENEMY3 = obj_Actor(24,24, 'alien2', ASSETS.S_ENEMY2,
                        creature = creature_com3, ai = ai_com3)

    # Keeps track of time
    CLOCK = pygame.time.Clock()

    ASSETS = struc_Assets()

    GAME.current_objects = [PLAYER, ENEMY, ENEMY1, ENEMY2]

if __name__ == '__main__':
    game_initialize()
    game_main_loop()
