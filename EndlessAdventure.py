import pygame as pg
from config import *
from _init__ import Character,Obstacle,screen,clock

def draw_bg():
    """
    Draws the background and moving ground for the game.

    This function fills the screen with the background color, draws the background image,
    and draws two ground images that move leftwards to create a continuous scrolling effect.
    Resets the ground position when the second ground image goes off-screen.-
    """
    screen.fill(BG)
    global ground1_x, ground2_x
    screen.blit(bg,(0,0))
    screen.blit(ground,(ground1_x,HEIGHT - 64))
    screen.blit(ground,(ground2_x,HEIGHT - 64))
    score_txt = font.render(f'Distance: {player.score}m', True, (255,255,255))
    score_rect = score_txt.get_rect(center = (WIDTH//2, 30))
    screen.blit(score_txt,score_rect)
    skyjump_txt = font.render(f'Skyjump: {player.skyjump}', True, (255,255,255))
    screen.blit(skyjump_txt,(10,15))
    ground1_x -=speed
    ground2_x -=speed
    if ground2_x <= 0:
        ground1_x = 0
        ground2_x = WIDTH

# Initialize Pygame
pg.init()

# Clock for controlling the frame rate
clock = pg.time.Clock()

# Initial positions of the ground images
ground1_x = 0
ground2_x = WIDTH
jump = False

# Load and scale images
bg=pg.transform.scale(pg.image.load(r'Image/background.png'),(WIDTH, HEIGHT))
ground=pg.transform.scale(pg.image.load(r'Image/ground.png'),(WIDTH, 64))

# Load font
font = pg.font.SysFont('sans',30)

# Create a player character
player = Character(250,295)
obstacles = pg.sprite.Group()
for _ in range(5):
    obstacle = Obstacle()
    obstacles.add(obstacle)

all_sprites = pg.sprite.Group(player, *obstacles)

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
    all_sprites.update()

    # Check for collisions
    if pg.sprite.spritecollide(player, obstacles, False):
        break
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
                if player.temp_skyjump > 1:
                    player.temp_skyjump -= 1
                    jump = True

        ## Keyboard released
        #if event.type == pg.KEYUP:
        #    if event.key == pg.K_SPACE or event.key == pg.K_UP:
        #        jump = False
    
    pg.display.update()