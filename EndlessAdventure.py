import pygame, random, sys, time
from config import *
from _init__ import Character,GameObject,screen,clock,OBJ_SIZE

def activate_shield():
    """
    Kích hoạt khiên bảo vệ và ghi lại thời gian bắt đầu kích hoạt.
    """
    global shield_active, shield_start_time
    shield_active = True
    shield_start_time = time.time()

def draw_button(screen, msg, x, y, w, h, ic, ac, action=None):
    """
    Vẽ nút bấm trên màn hình và kiểm tra sự kiện nhấn chuột.
    
    Tham số:
    - screen: Màn hình để vẽ nút.
    - msg: Thông điệp hiển thị trên nút.
    - x, y: Tọa độ của nút.
    - w, h: Chiều rộng và chiều cao của nút.
    - ic: Màu sắc của nút khi không được chọn.
    - ac: Màu sắc của nút khi được chọn.
    - action: Hành động khi nhấn nút.
    """
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
    """
    Tạo đối tượng văn bản.

    Tham số:
    - text: Nội dung văn bản.
    - font: Phông chữ của văn bản.

    Trả về:
    - textSurface: Bề mặt văn bản được render.
    - textRect: Hình chữ nhật bao quanh văn bản.
    """
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

def game_intro():
    """
    Hiển thị màn hình giới thiệu trò chơi.
    """
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
    """
    Thoát khỏi trò chơi.
    """
    pygame.quit()
    sys.exit()

def game_over_screen():
    """
    Hiển thị màn hình kết thúc trò chơi.
    """
    global game_intro_screen
    game_over_screen = True
    game_intro_screen = False
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
    Vẽ nền và mặt đất di chuyển cho trò chơi.
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

def create_game_obj():
    """
    Tạo các đối tượng trong trò chơi như chướng ngại vật và vật phẩm.
    """
    temp_x, temp_y =-1,-1
    for _ in range(5):
        orb = GameObject("obstacle")
        while True:
            if ((orb.rect.x + OBJ_SIZE) > temp_x > (orb.rect.x - OBJ_SIZE)) and ((orb.rect.y + OBJ_SIZE) > temp_y > (orb.rect.y - OBJ_SIZE)):
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
            if ((orb.rect.x + OBJ_SIZE) > temp_x > (orb.rect.x - OBJ_SIZE)) and ((orb.rect.y + OBJ_SIZE) > temp_y > (orb.rect.y - OBJ_SIZE)):
                orb = GameObject(orb_type)
                continue
            else:
                break
        temp_x, temp_y = orb.rect.x, orb.rect.y
        game_objects.add(orb)

def game_loop():
    """
    Vòng lặp chính của trò chơi.
    """
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

            # Nhấn phím
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

        # Cập nhật các đối tượng
        if len(game_objects)<=4:
            create_game_obj()
            all_sprites = pygame.sprite.Group(player, *game_objects)

        all_sprites.update()

        # Kiểm tra va chạm
        for obj in pygame.sprite.spritecollide(player, game_objects, False):
            if obj.type == "obstacle":
                if shield_active:
                    shield_active = False  # Sử dụng khiên
                elif player.lives > 1:
                    player.lives -= 1  # Mất một mạng
                else:
                    game_over_screen()  # Trò chơi kết thúc nếu không còn khiên và mạng
                obj.kill()
            elif obj.type == "shield":
                activate_shield()   # Nhận khiên
                obj.kill()
            elif obj.type == "extra_life":
                player.lives += 1   # Thêm mạng
                obj.kill()
            elif obj.type == "extra_jump":
                player.skyjump += 1 # Thêm sky jump
                obj.kill()

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
            player.update_action(1) # Nhảy
        elif player.velocity > 0 and player.rect.bottom < HEIGHT-60:
            player.update_action(2) # Rơi
        else:
            player.update_action(0) # Chạy
        jump = False

        font = pygame.font.SysFont('sans',30)
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
    """
    Hàm chính khởi tạo trò chơi.
    """
    pygame.init()
    global screen, clock, ground1_x, ground2_x, jump, shield_active, shield_duration, shield_start_time, SHIELD, GROUND, font, bg, all_sprites, speed, game_objects, player
    pygame.display.set_caption("Endless Adventure")
    clock = pygame.time.Clock()
    # Các thông số cơ bản của trò chơi
    ground1_x = 0
    ground2_x = WIDTH
    jump = False
    shield_active = False
    shield_duration = 5  # thời gian tồn tại của khiên tính bằng giây
    shield_start_time = 0

    # Tải và thay đổi kích thước hình ảnh
    bg=pygame.transform.scale(pygame.image.load(r'Image/background.png'),(WIDTH, HEIGHT))
    GROUND=pygame.transform.scale(pygame.image.load(r'Image/ground.png'),(WIDTH, 64))
    SHIELD=pygame.transform.scale(pygame.image.load(r'Image/shield_effect.png'),(OBJ_SIZE*4,OBJ_SIZE*4))

    # Tạo nhân vật người chơi
    player = Character(250,295)

    # Tạo các đối tượng trò chơi
    game_objects = pygame.sprite.Group()
    create_game_obj()
    all_sprites = pygame.sprite.Group(player, *game_objects)
    if game_intro_screen:
        game_intro()
    game_loop()

if __name__ == "__main__":
    game_intro_screen = True
    main()