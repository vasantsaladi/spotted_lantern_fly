import pygame
import pygame_menu
from random import randint
from pathlib import Path
from typing import Tuple


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)



# pygame setup
pygame.init()

# Define the stages of the game

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# interval to generate coins, time in MS
slf_countdown = 2500
slf_interval = 100

# Amount of SLFs allowed on screen
SLF_COUNT = 20

# Spotted Lanternfly class
class SpottedLanFly(pygame.sprite.Sprite):
    def __init__(self):
        super(SpottedLanFly, self).__init__()

        #get image path to draw for lanternfly
        slf_image = str(Path.cwd() / "slfGame" / "resources" / "images" / "slf_sprite.png")

        # Load the image, preserve alpha channel for transparency
        self.surf = pygame.image.load(slf_image).convert_alpha()
        sizeMod = randint(-100, 500) # Variable to modify the size of the Image
        self.surf = pygame.transform.scale(self.surf, (self.surf.get_width() - sizeMod, self.surf.get_height() - sizeMod))

        # Save the rect so you can move it
        self.rect = self.surf.get_rect()

        # Starting position
        self.rect = self.surf.get_rect(
            center=(
                randint(10, SCREEN_WIDTH - 10),
                randint(10, SCREEN_HEIGHT - 10),
            )
        )
        

# Render background for the Squash Level
def render_squash_background():
    screen.fill((83, 205, 255))

    #draw the ground
    pygame.draw.rect(screen, (36, 113, 20), pygame.Rect(0, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT/2))

    #insert the trees
    tree_img = pygame.image.load(str(Path.cwd() / "slfGame" / "resources" / "images" / "tree-3707718_1280.png")).convert_alpha()

    tree_img = pygame.transform.scale(tree_img, (tree_img.get_width()/2, tree_img.get_height()/2))

    #place first tree
    screen.blit(tree_img, (0, SCREEN_HEIGHT - tree_img.get_height()))

    #place second tree
    screen.blit(tree_img, (SCREEN_WIDTH - tree_img.get_width(), SCREEN_HEIGHT - tree_img.get_height()))


# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spotted Lanternfly Squash")
clock = pygame.time.Clock()

'''
def start_game():
    mainmenu._open(level)

mainmenu = pygame_menu.Menu('Welcome', 600, 400, theme= pygame_menu.themes.THEME_SOLARIZED)
mainmenu.add.text_input('Name: ', default='username', maxchar=20)
mainmenu.add.button('Play', start_game)
#mainmenu.add.button('Levels', level_menu)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

level = pygame_menu.Menu('Select a Difficulty', 600, 400, theme=pygame_menu.themes.THEME_BLUE)
level.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
'''
# a custom event to add a new SLF
ADDSLF = pygame.USEREVENT + 1
pygame.time.set_timer(ADDSLF, slf_countdown)

slf_list = pygame.sprite.Group()

score = 0

running = True
while running:
    # poll for events
    events = pygame.event.get()
    for event in events:
        # Player closed the game
        if event.type == pygame.QUIT:
            running = False


        elif event.type == ADDSLF:
            # Create a new moth and add it to the coin list
            new_slf = SpottedLanFly()
            slf_list.add(new_slf)

            if len(slf_list) < 3:
                slf_countdown -= slf_interval

            if slf_countdown < 100:
                slf_countdown = 100

            pygame.time.set_timer(ADDSLF, 0)
            pygame.time.set_timer(ADDSLF, slf_countdown)


    # RENDER YOUR GAME HERE

    # Are there too many coins on the screen?
    if len(slf_list) >= SLF_COUNT:
        # This counts as an end condition, so you end your game loop. It shuts down the game
        running = False

    render_squash_background()

    # Draw the slf next
    for slf in slf_list:
        screen.blit(slf.surf, slf.rect)


    # Finally, draw the score at the bottom left
    score_font = pygame.font.SysFont("any_font", 36)
    score_block = score_font.render(f"Score: {score}", False, (0, 0, 0))
    screen.blit(score_block, (50, SCREEN_HEIGHT - 50))

    ## Track the user's mouse position, and have it show up on screen.

    ## User's will click on a little moth, and be able to drag it around! Then they can like, idk do something to dispose of it

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()