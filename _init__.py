import pygame, random
from config import *

# Initialize the game screen and clock
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

# Load and scale images
obj_size = pygame.image.load(f'animation/run/0.png').get_height()//1.5
OBSTACLE_IMG = pygame.image.load("Image/bomb.png")
OBSTACLE_IMG = pygame.transform.scale(OBSTACLE_IMG, (obj_size,obj_size))
SHIELD_ORB_IMG = pygame.image.load("Image/shield.png")
SHIELD_ORB_IMG = pygame.transform.scale(SHIELD_ORB_IMG, (obj_size,obj_size))
EXTRA_LIFE_ORB_IMG = pygame.image.load("Image/extra_life.png")
EXTRA_LIFE_ORB_IMG = pygame.transform.scale(EXTRA_LIFE_ORB_IMG, (obj_size,obj_size))
EXTRA_JUMP_IMG = pygame.image.load("Image/extra_jump.png")
EXTRA_JUMP_IMG = pygame.transform.scale(EXTRA_JUMP_IMG, (obj_size,obj_size))

class Character(pygame.sprite.Sprite):
    """
    A class to represent a character in the game.

    Attributes
    ----------
    velocity : int
        The current vertical velocity of the character.
    __animation_list : list
        A list of lists containing the animation frames for different actions.
    __frame_index : int
        The current frame index of the animation.
    __action : int
        The current __action of the character (e.g., running, jumping, falling).
    __update_time_animation : int
        The time (in milliseconds) when the animation was last updated.
    image : pygame.Surface
        The current image/frame of the character.
    rect : pygame.Rect
        The rectangular area representing the character's position and size.

    Methods
    -------
    __init__(x, y, scale)
        Initializes the character with a position and scale.
    gravity()
        Applies gravity to the character.
    jump(jump)
        Makes the character jump if the jump parameter is True.
    update_animation()
        Updates the character's animation based on the current __action.
    update_action(new_action)
        Updates the character's __action and resets the animation if the __action changes.
    draw()
        Draws the character on the screen.
    """
    def __init__(self, x, y):
        """
        Initializes the character with a given position and scale.

        Parameters
        ----------
        x : int
            The x-coordinate of the character's position.
        y : int
            The y-coordinate of the character's position.
        scale : float
            The scale factor for the character's images.
        """
        pygame.sprite.Sprite.__init__(self)
        self.velocity = 0
        self.score = 0
        self.skyjump = 1
        self.temp_skyjump = self.skyjump
        self.lives = 1  # Lives attribute
        self.__animation_list = []
        self.__frame_index = 0
        self.__action = 1
        self.__update_time_animation = pygame.time.get_ticks()
        self.__update_time_score = pygame.time.get_ticks()
        temp_list = []

        for i in range(6):
            img = pygame.image.load(f'animation/run/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.__animation_list.append(temp_list)

        img = pygame.image.load(f'animation/jump/1.png')
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.__animation_list.append([img])

        img = pygame.image.load(f'animation/fall/0.png')
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.__animation_list.append([img])

        self.image = self.__animation_list[self.__action][self.__frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def gravity(self):
        """
        Applies gravity to the character, updating its vertical velocity and position.
        Prevents the character from moving above the top or below the bottom of the screen.
        """
        self.velocity += 0.25  # Gravity effect
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
        Makes the character jump by setting a negative vertical velocity.

        Parameters
        ----------
        jump : bool
            If True, the character will jump.
        """
        if jump:
            if self.rect.bottom < HEIGHT-50:
                self.temp_skyjump -= 1
            self.velocity = -7

    def update_animation(self):
        """
        Updates the character's animation frame based on the current __action and elapsed time.
        """
        ANIMATION_COOLDOWN = 150
        #update imgae depending on current frame
        self.image = self.__animation_list[self.__action][self.__frame_index]
        #chech if enough time has passed since the last update
        if pygame.time.get_ticks() - self.__update_time_animation > ANIMATION_COOLDOWN:
            self.__update_time_animation = pygame.time.get_ticks()
            self.__frame_index += 1
        #if the animation has run our the reset back to the start
        if self.__frame_index >= len(self.__animation_list[self.__action]):
            self.__frame_index = 0
    
    def update_score(self):
        SCORE_COOLDOWN = 300
        if pygame.time.get_ticks() - self.__update_time_score > SCORE_COOLDOWN:
            self.__update_time_score = pygame.time.get_ticks()
            self.score +=1

    def update_action(self, new_action):
        """
        Updates the character's __action and resets the animation if the __action changes.

        Parameters
        ----------
        new_action : int
            The new __action for the character.
        """
        #check if the new __action is different to the pervious one
        if new_action != self.__action:
            self.__action = new_action
            #update the animation settings
            self.__frame_index = 0
            self.__update_time_animation = pygame.time.get_ticks()

    def draw(self):
        """
        Draws the character on the screen.
        """
        screen.blit(self.image, self.rect)

class GameObject(pygame.sprite.Sprite):
    """
    A class to represent various objects in the game, including obstacles and orbs.

    Attributes
    ----------
    type : str
        The type of the game object, which can be "obstacle", "shield", or "extra_life".
    image : pygame.Surface
        The image representing the game object.
    rect : pygame.Rect
        The rectangular area representing the game object's position and size.

    Methods
    -------
    __init__(obj_type)
        Initializes the game object with a specific type.
    update()
        Updates the position of the game object, moving it leftwards across the screen.
    """
    def __init__(self, obj_type):
        """
        Initializes the game object with a specific type.

        Parameters
        ----------
        obj_type : str
            The type of the game object, which determines its appearance and behavior.
            Possible values are "obstacle", "shield", and "extra_life".
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
        Updates the position of the game object, moving it leftwards across the screen.
        Resets the object's position when it moves off the left side of the screen.
        """
        global speed
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()