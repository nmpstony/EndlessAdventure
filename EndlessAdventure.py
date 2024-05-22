import pygame as pg
from config import *
from _init__ import Character,screen,clock
#from _init__ import
def draw_bg():
    screen.fill(BG)
    global ground1_x, ground2_x
    screen.blit(bg,(0,0))
    screen.blit(ground,(ground1_x,HEIGHT - 64))
    screen.blit(ground,(ground2_x,HEIGHT - 64))
    ground1_x -=speed
    ground2_x -=speed
    if ground2_x <= 0:
        ground1_x = 0
        ground2_x = WIDTH


pg.init()


clock = pg.time.Clock()

ground1_x = 0
ground2_x = WIDTH
jump = False

bg=pg.transform.scale(pg.image.load(r'Image/background.png'),(WIDTH, HEIGHT))
ground=pg.transform.scale(pg.image.load(r'Image/ground.png'),(WIDTH, 64))

player = Character(250,295,1.5,2)





while True:

    clock.tick(FPS)

    draw_bg()

    player.update_animation()
    player.draw()

    player.move(jump)

    if jump:
        player.update_action(1)#jump
    else:
        player.update_action(0)#run

    for event in pg.event.get():
        #quit game
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        #keyborad presses
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE or event.key == pg.K_UP:
                jump = True

        #keyboard released
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE or event.key == pg.K_UP:
                jump = False
    
    pg.display.update()