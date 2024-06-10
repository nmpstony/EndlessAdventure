import pygame, random, sys, time
from config import *
from _init__ import Character,GameObject,screen,clock,obj_size

def activate_shield():
    global shield_active, shield_start_time
    shield_active = True
    shield_start_time = time.time()

def draw_button(screen, msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(bg, (0,0))
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("Endless Adventure", largeText)
        TextRect.center = ((WIDTH / 2), (HEIGHT // 3))
        screen.blit(TextSurf, TextRect)

        draw_button(screen, "Play", WIDTH//2-50, 200, 100, 50, green, bright_green, game_loop)
        draw_button(screen, "Quit", WIDTH//2-50, 260, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)

def quit_game():
    pygame.quit()
    sys.exit()

def game_over_screen():
    game_over_screen = True

    while game_over_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(bg, (0,0))
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("Game Over", largeText)
        TextRect.center = ((WIDTH / 2), (HEIGHT // 3))
        screen.blit(TextSurf, TextRect)

        draw_button(screen, "Play Again", WIDTH//2-75, 200, 150, 50, green, bright_green, main)
        draw_button(screen, "Quit", WIDTH//2-50, 260, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)

def draw_bg():
    """
    Draws the background and moving ground for the game.

    This function fills the screen with the background color, draws the background image,
    and draws two ground images that move leftwards to create a continuous scrolling effect.
    Resets the ground position when the second ground image goes off-screen.-
    """
    global ground1_x, ground2_x, speed
    screen.blit(bg,(0,0))
    screen.blit(GROUND,(ground1_x,HEIGHT - 64))
    screen.blit(GROUND,(ground2_x,HEIGHT - 64))
    ground1_x -= speed
    ground2_x -= speed
    if ground2_x <= 0:
        ground1_x = 0
        ground2_x = WIDTH

# Create game object
def create_game_obj():
    temp_x, temp_y =-1,-1
    for _ in range(5):
        orb = GameObject("obstacle")
        while True:
            if ((orb.rect.x + obj_size) > temp_x > (orb.rect.x - obj_size)) and ((orb.rect.y + obj_size) > temp_y > (orb.rect.y - obj_size)):
                orb = GameObject("obstacle")
                continue
            else:
                break
        temp_x, temp_y = orb.rect.x, orb.rect.y
        game_objects.add(orb)

    for _ in range(3):
        if player.skyjump <=3:
            orb_type = random.choice(["shield"]*2 + ["extra_life"]*2 + ["extra_jump"])
        else:
            orb_type = random.choice(["shield", "shield", "extra_life"])
        
        orb = GameObject(orb_type)
        while True:
            if ((orb.rect.x + obj_size) > temp_x > (orb.rect.x - obj_size)) and ((orb.rect.y + obj_size) > temp_y > (orb.rect.y - obj_size)):
                orb = GameObject(orb_type)
                continue
            else:
                break
        temp_x, temp_y = orb.rect.x, orb.rect.y
        game_objects.add(orb)


def game_loop():
    global jump, all_sprites, shield_active, shield_start_time
    game_exit = False
    game_over = False
    while not game_exit:

        while game_over:
            game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard presses
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    if player.temp_skyjump > 0:
                        jump = True

        draw_bg()

        player.update_animation()
        player.draw()
        player.update_score()
        player.gravity()
        player.jump(jump)

        # Update
        if len(game_objects)<=4:
            create_game_obj()
            all_sprites = pygame.sprite.Group(player, *game_objects)

        all_sprites.update()

        # Check for collisions
        for obj in pygame.sprite.spritecollide(player, game_objects, False):
            if obj.type == "obstacle":
                if shield_active:
                    shield_active = False  # Use the shield
                elif player.lives > 1:
                    player.lives -= 1  # Lose a life
                else:
                    game_over_screen()  # Game over if no shield and no extra life
                obj.kill()
            elif obj.type == "shield":
                activate_shield()
                obj.kill()  # Remove the orb
            elif obj.type == "extra_life":
                player.lives += 1
                obj.kill()  # Remove the orb
            elif obj.type == "extra_jump":
                player.skyjump += 1
                obj.kill()  # Remove the orb

        all_sprites.draw(screen)

        if shield_active:
            current_time = time.time()
            elapsed_time = current_time - shield_start_time
            if elapsed_time > shield_duration:
                shield_active = False
            else:
                # Hiển thị thời gian còn lại của khiên trên màn hình
                rect1 = pygame.draw.rect(screen, black, (player.rect.x-45, player.rect.y-40,120,20))
                rect2 = pygame.draw.rect(screen, white, (player.rect.x-40, player.rect.y-35,(shield_duration - int(elapsed_time))*110/5,10))
            SHIELD_RECT=SHIELD.get_rect()
            SHIELD_RECT.center=(player.rect.center)
            screen.blit(SHIELD, SHIELD_RECT)

        if player.velocity < 0:
            player.update_action(1) #Jump
        elif player.velocity > 0 and player.rect.bottom < HEIGHT-60:
            player.update_action(2) #Fall
        else:
            player.update_action(0) #Run
        jump = False

        score_txt = font.render(f'Distance: {player.score}m', True, color_text)
        score_rect = score_txt.get_rect(center = (WIDTH//2, 30))
        screen.blit(score_txt,score_rect)
        skyjump_txt = font.render(f'Skyjump: {player.temp_skyjump}', True, color_text)
        screen.blit(skyjump_txt,(10,15))
        lives_txt = font.render(f'Lives: {player.lives}', True, color_text)
        screen.blit(lives_txt,(10,50))
        
        pygame.display.update()
        clock.tick(FPS)

def main():
    pygame.init()
    global screen, clock, ground1_x, ground2_x, jump, color_text, shield_active, shield_duration, shield_start_time, SHIELD, GROUND, font, bg, all_sprites, speed, game_objects, player
    pygame.display.set_caption("Endless Adventure")
    clock = pygame.time.Clock()
    # Initial positions of the ground images
    ground1_x = 0
    ground2_x = WIDTH
    jump = False
    color_text = (0,0,0)
    shield_active = False
    shield_duration = 5  # thời gian tồn tại của khiên tính bằng giây
    shield_start_time = 0

    # Load and scale images
    bg=pygame.transform.scale(pygame.image.load(r'Image/background.png'),(WIDTH, HEIGHT))
    GROUND=pygame.transform.scale(pygame.image.load(r'Image/ground.png'),(WIDTH, 64))
    SHIELD=pygame.transform.scale(pygame.image.load(r'Image/shield_effect.png'),(obj_size*4,obj_size*4))

    # Load font
    font = pygame.font.SysFont('sans',30)

    # Create a player character
    player = Character(250,295)

    # Create game objects
    game_objects = pygame.sprite.Group()
    create_game_obj()
    all_sprites = pygame.sprite.Group(player, *game_objects)
    game_intro()
    game_loop()

if __name__ == "__main__":
    main()