import pygame
from pygame.locals import *
from foreverdrive.shapes import MovingBox
from foreverdrive.area import TileArea

pygame.init()

screen = pygame.display.set_mode((500, 500))

area = TileArea("default_tile.png", (10, 10))

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
                area.top -= 1
            elif event.key == K_DOWN:
                area.top += 1
            elif event.key == K_LEFT:
                area.left -= 1
            elif event.key == K_RIGHT:
                area.left += 1

    ticks = pygame.time.get_ticks()

    tg = area.tile_group
    tg.update(ticks)

    rectlist = tg.draw(screen)
    pygame.display.update(rectlist)

