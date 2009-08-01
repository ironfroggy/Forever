import pygame
from pygame.locals import *
from foreverdrive.shapes import MovingBox
from foreverdrive.area import TileArea

pygame.init()

screen = pygame.display.set_mode((500, 500))
background = pygame.Surface((500, 500))
background.fill((0, 0, 0))
screen.blit(background, (0, 0))

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

    tg = area.tile_group
    tg.update(pygame.time.get_ticks())
    rectlist = tg.draw(screen)
    pygame.display.update(rectlist)
    tg.clear(screen, background)
