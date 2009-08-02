import pygame
from pygame.locals import *
from foreverdrive.shapes import UpDownBox

pygame.init()
boxes = pygame.sprite.Group()
for color, location in [([255, 0, 0], [0, 0]),
                        ([0, 255, 0], [60, 60]),
                        ([0, 0, 255], [120, 120])]:
    boxes.add(UpDownBox(color, location))

screen = pygame.display.set_mode([150, 150])
while pygame.event.poll().type != KEYDOWN:
    screen.fill([0, 0, 0]) # blank the screen.
    boxes.update(pygame.time.get_ticks(), 150)
    for b in boxes.sprites():
        screen.blit(b.image, b.rect)
    pygame.display.update()
