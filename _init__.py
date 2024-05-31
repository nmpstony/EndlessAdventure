import pygame as pg
from config import *

# Initialize the game screen and clock
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()

class Character(pg.sprite.Sprite):
    """
    A class to represent a character in the game.

    Attributes
    ----------
    velocity : int
        The current vertical velocity of the character.
    animation_list : list
        A list of lists containing the animation frames for different actions.
    frame_index : int
        The current frame index of the animation.
    action : int
        The current action of the character (e.g., running, jumping, falling).
    update_time_animation : int
        The time (in milliseconds) when the animation was last updated.
    update_time_jump : int
        The time (in milliseconds) when the jump was last updated.
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
        Updates the character's animation based on the current action.
    update_action(new_action)
        Updates the character's action and resets the animation if the action changes.
    draw()
        Draws the character on the screen.
    """
    def __init__(self, x, y, scale):
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
        pg.sprite.Sprite.__init__(self)
        self.velocity = 0
        self.animation_list = []
        self.frame_index = 0
        self.action = 1
        self.update_time_animation = pg.time.get_ticks()
        self.update_time_jump = pg.time.get_ticks()
        temp_list = []

        for i in range(6):
            img = pg.image.load(f'animation/run/{i}.png')
            img = pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        img = pg.image.load(f'animation/jump/1.png')
        img = pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.animation_list.append([img])

        img = pg.image.load(f'animation/fall/0.png')
        img = pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.animation_list.append([img])

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def gravity(self):
        """
        Applies gravity to the character, updating its vertical velocity and position.
        Prevents the character from moving above the top or below the bottom of the screen.
        """
        self.velocity += 1  # Gravity effect
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= HEIGHT-50:
            self.rect.bottom = HEIGHT-50
            self.velocity = 0

    def jump(self,jump):
        """
        Makes the character jump by setting a negative vertical velocity.

        Parameters
        ----------
        jump : bool
            If True, the character will jump.
        """
        if jump:
            self.velocity = -10

    def update_animation(self):
        """
        Updates the character's animation frame based on the current action and elapsed time.
        """
        ANIMATION_COOLDOWN = 150
        JUMP_TIME = 20
        #update imgae depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #chech if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time_animation > ANIMATION_COOLDOWN:
            self.update_time_animation = pg.time.get_ticks()
            self.frame_index += 1
        #if the animation has run our the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0


    def update_action(self, new_action):
        """
        Updates the character's action and resets the animation if the action changes.

        Parameters
        ----------
        new_action : int
            The new action for the character.
        """
        #check if the new action is different to the pervious one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time_animation = pg.time.get_ticks()

    def draw(self):
        """
        Draws the character on the screen.
        """
        screen.blit(self.image, self.rect)