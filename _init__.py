import pygame, random
from config import *

# Khởi tạo màn hình trò chơi và đồng hồ
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

# Tải và thay đổi kích thước hình ảnh
OBJ_SIZE = pygame.image.load(f'animation/run/0.png').get_height()//1.5
OBSTACLE_IMG = pygame.image.load("Image/bomb.png")
OBSTACLE_IMG = pygame.transform.scale(OBSTACLE_IMG, (OBJ_SIZE,OBJ_SIZE))
SHIELD_ORB_IMG = pygame.image.load("Image/shield.png")
SHIELD_ORB_IMG = pygame.transform.scale(SHIELD_ORB_IMG, (OBJ_SIZE,OBJ_SIZE))
EXTRA_LIFE_ORB_IMG = pygame.image.load("Image/extra_life.png")
EXTRA_LIFE_ORB_IMG = pygame.transform.scale(EXTRA_LIFE_ORB_IMG, (OBJ_SIZE,OBJ_SIZE))
EXTRA_JUMP_IMG = pygame.image.load("Image/extra_jump.png")
EXTRA_JUMP_IMG = pygame.transform.scale(EXTRA_JUMP_IMG, (OBJ_SIZE,OBJ_SIZE))

class Character(pygame.sprite.Sprite):
    """
    Lớp đại diện cho nhân vật trong trò chơi.

    Thuộc tính
    ----------
    velocity : int
        Tốc độ dọc hiện tại của nhân vật.
    __animation_list : list
        Danh sách các khung hình cho các hành động khác nhau của nhân vật.
    __frame_index : int
        Chỉ số khung hình hiện tại của hoạt ảnh.
    __action : int
        Hành động hiện tại của nhân vật (chạy, nhảy, rơi).
    __update_time_animation : int
        Thời gian (tính bằng mili giây) khi hoạt ảnh được cập nhật lần cuối.
    image : pygame.Surface
        Hình ảnh hiện tại của nhân vật.
    rect : pygame.Rect
        Hình chữ nhật đại diện cho vị trí và kích thước của nhân vật.

    Phương thức
    -------
    __init__(x, y)
        Khởi tạo nhân vật với vị trí và tỉ lệ.
    gravity()
        Áp dụng trọng lực lên nhân vật.
    jump(jump)
        Khiến nhân vật nhảy nếu tham số jump là True.
    update_animation()
        Cập nhật hoạt ảnh của nhân vật dựa trên hành động hiện tại.
    update_action(new_action)
        Cập nhật hành động của nhân vật và đặt lại hoạt ảnh nếu hành động thay đổi.
    draw()
        Vẽ nhân vật lên màn hình.
    """
    def __init__(self, x, y):
        """
        Khởi tạo nhân vật với vị trí và tỉ lệ nhất định.

        Tham số
        ----------
        x : int
            Tọa độ x của vị trí nhân vật.
        y : int
            Tọa độ y của vị trí nhân vật.
        """
        pygame.sprite.Sprite.__init__(self)
        self.velocity = 0
        self.score = 0
        self.skyjump = 1
        self.temp_skyjump = self.skyjump
        self.lives = 1
        self.__animation_list = []
        self.__frame_index = 0
        self.__action = 1
        self.__update_time_animation = pygame.time.get_ticks()
        self.__update_time_score = pygame.time.get_ticks()
        temp_list = []

        # Tải hoạt ảnh chạy
        for i in range(6):
            img = pygame.image.load(f'animation/run/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.__animation_list.append(temp_list)

        # Tải hoạt ảnh nhảy
        img = pygame.image.load(f'animation/jump/1.png')
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.__animation_list.append([img])

        # Tải hoạt ảnh rơi
        img = pygame.image.load(f'animation/fall/0.png')
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.__animation_list.append([img])

        self.image = self.__animation_list[self.__action][self.__frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def gravity(self):
        """
        Áp dụng trọng lực lên nhân vật, cập nhật tốc độ dọc và vị trí của nó.
        Ngăn nhân vật di chuyển lên trên hoặc xuống dưới màn hình.
        """
        self.velocity += 0.25  # Hiệu ứng trọng lực
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = -0.25
        if self.rect.bottom >= HEIGHT-50:
            self.rect.bottom = HEIGHT-50
            self.velocity = 0
            self.temp_skyjump = self.skyjump


    def jump(self,jump):
        """
        Khiến nhân vật nhảy bằng cách đặt tốc độ dọc thành giá trị âm.

        Tham số
        ----------
        jump : bool
            Nếu True, nhân vật sẽ nhảy.
        """
        if jump:
            if self.rect.bottom < HEIGHT-50:
                self.temp_skyjump -= 1
            self.velocity = -7  # Sức bật của cú nhảy

    def update_animation(self):
        """
        Cập nhật khung hình hoạt ảnh của nhân vật dựa trên hành động hiện tại và thời gian đã trôi qua.
        """
        ANIMATION_COOLDOWN = 150
        # Cập nhật hình ảnh dựa trên khung hình hiện tại
        self.image = self.__animation_list[self.__action][self.__frame_index]
        # Kiểm tra nếu đủ thời gian đã trôi qua từ lần cập nhật cuối
        if pygame.time.get_ticks() - self.__update_time_animation > ANIMATION_COOLDOWN:
            self.__update_time_animation = pygame.time.get_ticks()
            self.__frame_index += 1
        # Nếu hoạt ảnh đã chạy hết, đặt lại về khung hình đầu tiên
        if self.__frame_index >= len(self.__animation_list[self.__action]):
            self.__frame_index = 0
    
    def update_score(self):
        """
        Cập nhật điểm số của nhân vật dựa trên thời gian đã trôi qua.
        """
        SCORE_COOLDOWN = 300
        if pygame.time.get_ticks() - self.__update_time_score > SCORE_COOLDOWN:
            self.__update_time_score = pygame.time.get_ticks()
            self.score +=1

    def update_action(self, new_action):
        """
        Cập nhật hành động của nhân vật và đặt lại hoạt ảnh nếu hành động thay đổi.

        Tham số
        ----------
        new_action : int
            Hành động mới của nhân vật.
        """
        # Kiểm tra nếu hành động mới khác với hành động trước đó
        if new_action != self.__action:
            self.__action = new_action
            # Cập nhật cài đặt hoạt ảnh
            self.__frame_index = 0
            self.__update_time_animation = pygame.time.get_ticks()

    def draw(self):
        """
        Vẽ hình ảnh lên màn hình.
        """
        screen.blit(self.image, self.rect)

class GameObject(pygame.sprite.Sprite):
    """
    Lớp đại diện cho các đối tượng trong trò chơi, bao gồm chướng ngại vật và vật phẩm.

    Thuộc tính
    ----------
    type : str
        Loại đối tượng trò chơi, có thể là "obstacle", "shield", hoặc "extra_life".
    image : pygame.Surface
        Hình ảnh đại diện cho đối tượng trò chơi.
    rect : pygame.Rect
        Hình chữ nhật đại diện cho vị trí và kích thước của đối tượng trò chơi.

    Phương thức
    -------
    __init__(obj_type)
        Khởi tạo đối tượng trò chơi với một loại cụ thể.
    update()
        Cập nhật vị trí của đối tượng trò chơi, di chuyển nó sang trái màn hình.
    """
    def __init__(self, obj_type):
        """
        Khởi tạo đối tượng trò chơi với một loại cụ thể.

        Tham số
        ----------
        obj_type : str
            Loại đối tượng trò chơi, quyết định hình ảnh và hành vi của nó.
            Các giá trị có thể là "obstacle", "shield", và "extra_life".
        """
        super().__init__()
        self.type = obj_type
        if self.type == "obstacle":
            self.image = OBSTACLE_IMG
        elif self.type == "shield":
            self.image = SHIELD_ORB_IMG
        elif self.type == "extra_life":
            self.image = EXTRA_LIFE_ORB_IMG
        elif self.type == "extra_jump":
            self.image = EXTRA_JUMP_IMG
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH, 3 * WIDTH)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height - 60)

    def update(self):
        """
        Cập nhật vị trí của đối tượng trò chơi, di chuyển nó sang trái màn hình.
        Đặt lại vị trí của đối tượng khi nó di chuyển ra khỏi phía bên trái màn hình.
        """
        global speed
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()