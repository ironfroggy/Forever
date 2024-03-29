import pygame
from pygame.locals import *
from foreverdrive.shapes import UpDownBox

pygame.init()
boxes = pygame.sprite.RenderUpdates()
for color, location in [([255, 0, 0], [0, 0]),
		        ([0, 255, 0], [60, 60]),
                        ([0, 0, 255], [120, 120])]:
    boxes.add(UpDownBox(color, location))

screen = pygame.display.set_mode([150, 150])
background = pygame.Surface([150, 150])
background.fill([0, 0, 0])
screen.blit(background, [0, 0])
while pygame.event.poll().type != KEYDOWN:
    boxes.update(pygame.time.get_ticks(), 150)
    rectlist = boxes.draw(screen)
    pygame.display.update(rectlist)
#    pygame.time.delay(10)
    boxes.clear(screen, background)
