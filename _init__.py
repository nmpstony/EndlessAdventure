import pygame as pg
from config import *

screen = pg.display.set_mode((WIDTH,HEIGHT))
#set framerate
clock = pg.time.Clock()

class Character(pg.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pg.sprite.Sprite.__init__(self)
        self.speed = speed
        self.animation_list = []
        self.frame_index = 0
        self.action = 1
        self.update_time = pg.time.get_ticks()
        temp_list = []
        for i in range(2):
            img = pg.image.load(f'animation/idle/{i}.png')
            img = pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(6):
            img = pg.image.load(f'animation/run/{i}.png')
            img = pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)


    def move(self, jump):
        dy = 0
        if jump:
            dy = -self.speed
        self.rect.y += dy

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update imgae depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #chech if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
        #if the animation has run our the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0


    def update_action(self, new_action):
        #check if the new action is different to the pervious one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()
            
    def draw(self):
        screen.blit(self.image, self.rect)