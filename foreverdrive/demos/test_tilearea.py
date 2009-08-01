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

boxes = pygame.sprite.RenderUpdates()
box = MovingBox((128, 128, 128), (200, 200))
boxes.add(box)

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

    ticks = pygame.time.get_ticks()

    tg = area.tile_group
    tg.update(ticks)
    boxes.update(ticks)

    rectlist = tg.draw(screen)
    pygame.display.update(rectlist + boxes.draw(screen))

#   tg.clear(screen, background)
#    boxes.clear(screen, background)
