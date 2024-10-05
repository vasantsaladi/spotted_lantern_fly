import pygame

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

from random import randint
from pathlib import Path
from typing import Tuple

# pygame setup
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# interval to generate coins, time in MS
slf_countdown = 2500
slf_interval = 100

# Amount of SLFs allowed on screen
SLF_COUNT = 10

class SpottedLanFly(pygame.sprite.Sprite):
    def __init__(self):
        super(SpottedLanFly, self).__init__()

        #get image to draw for lanternfly
        slf_image = str(Path.cwd() / "slfGame" / "resources" / "images" / "slf_sprite.png")

        # Load the image, preserve alpha channel for transparency
        self.surf = pygame.image.load(slf_image).convert_alpha()

        # Save the rect so you can move it
        self.rect = self.surf.get_rect()

        # The starting position is randomly generated

        self.rect = self.surf.get_rect(
            center=(
                randint(10, SCREEN_WIDTH - 10),
                randint(10, SCREEN_HEIGHT - 10),
            )
        )
        

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# a custom event to add a new SLF
ADDSLF = pygame.USEREVENT + 1
pygame.time.set_timer(ADDSLF, slf_countdown)

slf_list = pygame.sprite.Group()

score = 0

running = True
while running:
    # poll for events
    for event in pygame.event.get():
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
        # This counts as an end condition, so you end your game loop
        running = False

    # To render the screen, first fill the background with a color to wipe away anything from last frame
    screen.fill("purple")

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