import pygame as pg
import random
from config import *
from _init__ import Character,GameObject,screen,clock,obj_size

def draw_bg():
    """
    Draws the background and moving ground for the game.

    This function fills the screen with the background color, draws the background image,
    and draws two ground images that move leftwards to create a continuous scrolling effect.
    Resets the ground position when the second ground image goes off-screen.-
    """
    global ground1_x, ground2_x
    screen.blit(bg,(0,0))
    screen.blit(GROUND,(ground1_x,HEIGHT - 64))
    screen.blit(GROUND,(ground2_x,HEIGHT - 64))
    score_txt = font.render(f'Distance: {player.score}m', True, (255,255,255))
    score_rect = score_txt.get_rect(center = (WIDTH//2, 30))
    screen.blit(score_txt,score_rect)
    skyjump_txt = font.render(f'Skyjump: {player.temp_skyjump}', True, (255,255,255))
    screen.blit(skyjump_txt,(10,15))
    ground1_x -=speed
    ground2_x -=speed
    if ground2_x <= 0:
        ground1_x = 0
        ground2_x = WIDTH

# Create game object
def create_game_obj():
    global game_objects
    temp_x, temp_y =-1,-1
    for _ in range(5):
        game_object = GameObject("obstacle")
        while True:
            if game_object.rect.x == temp_x and game_object.rect.y == temp_y:
                game_object = GameObject("obstacle")
                continue
            else:
                break
        temp_x, temp_y = game_object.rect.x, game_object.rect.y
        game_objects.add(game_object)

    for _ in range(4):
        orb_type = random.choice(["shield", "extra_life"])
        orb = GameObject(orb_type)
        while True:
            if orb.rect.x == temp_x and orb.rect.y == temp_y:
                orb = GameObject(orb_type)
                continue
            else:
                break
        temp_x, temp_y = orb.rect.x, orb.rect.y
        game_objects.add(orb)

# Initialize Pygame
pg.init()

# Clock for controlling the frame rate
clock = pg.time.Clock()

# Initial positions of the ground images
ground1_x = 0
ground2_x = WIDTH
jump = False
count = 0


# Load and scale images
bg=pg.transform.scale(pg.image.load(r'Image/background.png'),(WIDTH, HEIGHT))
GROUND=pg.transform.scale(pg.image.load(r'Image/ground.png'),(WIDTH, 64))
SHIELD=pg.transform.scale(pg.image.load(r'Image/shield_effect.png'),(obj_size*4,obj_size*4))
SHIELD_RECT=SHIELD.get_rect()

# Load font
font = pg.font.SysFont('sans',30)

# Create a player character
player = Character(250,295)

# Create game objects
game_objects = pg.sprite.Group()
create_game_obj()
all_sprites = pg.sprite.Group(player, *game_objects)

while True:
    """
    Main game loop.

    This loop handles the frame rate, background drawing, character animation and movement,
    user input for jumping, and updating the display. The loop continues until the game is quit.
    """
    clock.tick(FPS)

    draw_bg()

    player.update_animation()
    player.draw()
    player.update_score()
    player.gravity()
    player.jump(jump)
    
    # Update
    if len(game_objects)<=4:
        create_game_obj()
        all_sprites = pg.sprite.Group(player, *game_objects)

    all_sprites.update()

    # Check for collisions
    for obj in pg.sprite.spritecollide(player, game_objects, False):
        if obj.type == "obstacle":
            if player.shield:
                player.shield = False  # Use the shield
            elif player.lives > 1:
                player.lives -= 1  # Lose a life
            else:
                pg.quit()
                exit()  # Game over if no shield and no extra life
            obj.kill()
        elif obj.type == "shield":
            player.shield = True
            obj.kill()  # Remove the orb
        elif obj.type == "extra_life":
            player.lives += 1
            obj.kill()  # Remove the orb

    all_sprites.draw(screen)

    if player.velocity < 0:
        player.update_action(1) #Jump
    elif player.velocity > 0 and player.rect.bottom < HEIGHT-60:
        player.update_action(2) #Fall
    else:
        player.update_action(0) #Run
    jump = False
    for event in pg.event.get():
        # Quit game
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # Keyboard presses
        if event.type == pg.KEYDOWN:
            if (event.key == pg.K_SPACE or event.key == pg.K_UP):
                if player.temp_skyjump > 0:
                    jump = True

    if player.shield:
    
        SHIELD_RECT.center=(player.rect.center)
        screen.blit(SHIELD, SHIELD_RECT)
    pg.display.update()