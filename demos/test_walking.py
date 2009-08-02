import pygame
from pygame.locals import *
from foreverdrive.shapes import MovingBox

pygame.init()
boxes = pygame.sprite.RenderUpdates()
box = MovingBox((128, 128, 128), (200, 200))
boxes.add(box)

screen = pygame.display.set_mode([500, 500])
background = pygame.Surface([500, 500])
background.fill([0, 0, 0])
screen.blit(background, [0, 0])

quit = False
while not quit:
    #Handle Input Events
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True
            break
        elif event.type == KEYUP and event.key == K_ESCAPE:
            quit = True
            break
        elif event.type == KEYUP and event.key == K_F10:
            import pdb
            pdb.set_trace()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                box.move_up()
            elif event.key == K_DOWN:
                box.move_down()
            elif event.key == K_LEFT:
                box.move_left()
            elif event.key == K_RIGHT:
                box.move_right()

    boxes.update(pygame.time.get_ticks())
    rectlist = boxes.draw(screen)
    pygame.display.update(rectlist)
    boxes.clear(screen, background)
