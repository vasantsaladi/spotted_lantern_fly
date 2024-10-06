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
        sizeMod = randint(-100, 400) # Variable to modify the size of the Image
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
        
# Player Class for Squash Game
class PlayerHand(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerHand, self).__init__()

        #player_image = str(Path.cwd() / "slfGame" / "resources" / "images" / "handopen.png")
        self.images = [str(Path.cwd() / "slfGame" / "resources" / "images" / "handopen.png"), str(Path.cwd() / "slfGame" / "resources" / "images" / "handclosed.png")]
        
        self.surf_open = pygame.image.load(self.images[0]).convert_alpha()
        self.surf_open = pygame.transform.scale(self.surf_open, (self.surf_open.get_width()/20, self.surf_open.get_height()/20)) #resize image

        self.surf_closed = pygame.image.load(self.images[1]).convert_alpha()
        self.surf_closed = pygame.transform.scale(self.surf_closed, (self.surf_closed.get_width()/20, self.surf_closed.get_height()/20)) #resize image

        self.surf = self.surf_open
        self.rect = self.surf.get_rect()

    # Update player position. pos{Tuple} -- X,Y position to move player to
    def update(self, pos: Tuple):
        self.rect.center = pos
    
    # Update player sprite. open{bool} -- true if opening image
    def update_sprite_open(self, open: bool):
        if open:
            self.surf = self.surf_open
            #self.rect = self.surf.get_rect()
        else:
            self.surf = self.surf_closed
            #self.rect = self.surf.get_rect()





# Render background for the Squash Level
def render_squash_background():
    screen.fill((83, 205, 255))

    #draw the ground
    #pygame.draw.rect(screen, (36, 113, 20), pygame.Rect(0, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT/2))
    background_img = pygame.image.load(str(Path.cwd() / "slfGame" / "resources" / "images" / "grassScene.jpg"))
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.blit(background_img, (0, 0))

    # set up tree images
    tree_img = pygame.image.load(str(Path.cwd() / "slfGame" / "resources" / "images" / "tree-3707718_1280.png")).convert_alpha()
    tree_img = pygame.transform.scale(tree_img, (tree_img.get_width()/2, tree_img.get_height()/2))

    # place trees
    screen.blit(tree_img, (0, SCREEN_HEIGHT - tree_img.get_height()))
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
pygame.mouse.set_visible(False)

# Create player sprite and set start position
player = PlayerHand()
player.update(pygame.mouse.get_pos())


# Set up Sound effects
moth_flapping_sound = pygame.mixer.Sound(str(Path.cwd() / "slfGame" / "resources" / "sounds" / "light-wing-flap-6143.mp3"))

moth_pop_sound = pygame.mixer.Sound(str(Path.cwd() / "slfGame" / "resources" / "sounds" / "pick-92276.mp3"))

running = True
while running:
    # poll for events
    events = pygame.event.get()
    for event in events:
        # Player closed the game
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            # quit game on escape
            if event.key == K_ESCAPE:
                running = False


        elif event.type == ADDSLF:
            # Create a new moth and add it to the slf list
            new_slf = SpottedLanFly()
            slf_list.add(new_slf)
            moth_flapping_sound.play()

            if len(slf_list) < 3:
                slf_countdown -= slf_interval

            if slf_countdown < 100:
                slf_countdown = 100

            pygame.time.set_timer(ADDSLF, 0)
            pygame.time.set_timer(ADDSLF, slf_countdown)


    # RENDER YOUR GAME HERE
    player.update(pygame.mouse.get_pos())

    if pygame.mouse.get_pressed()[0]:
        player.update_sprite_open(False)
        slf_killed = pygame.sprite.spritecollide(sprite=player, group=slf_list, dokill=True)
        for slf in slf_killed:
            score += 1
            moth_pop_sound.play()
    else:
        player.update_sprite_open(True)
        
    


    # Are there too many coins on the screen?
    if len(slf_list) >= SLF_COUNT:
        # This counts as an end condition, so you end your game loop. It shuts down the game
        running = False

    render_squash_background()

    # Draw the slf
    for slf in slf_list:
        screen.blit(slf.surf, slf.rect)

    # Draw Player
    screen.blit(player.surf, player.rect)

    # Finally, draw the score at the bottom left
    score_font = pygame.font.SysFont("any_font", 36)
    score_block = score_font.render(f"Score: {score}", False, (83, 205, 255))
    screen.blit(score_block, (50, SCREEN_HEIGHT - 50))

    ## User's will click on a little moth, and be able to drag it around! Then they can like, idk do something to dispose of it

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.mouse.set_visible(True)
pygame.quit()