import pygame
from pygame.locals import *
from foreverdrive.shapes import UpDownBox

pygame.init()
boxes = []
for color, location in [([255, 0, 0], [0, 0]),
                        ([255, 128, 0], [15, 15]),
                        ([255, 255, 0], [30, 30]),
                        ([128, 255, 0], [45, 45]),
                        ([0, 255, 0], [60, 60]),
                        ([0, 255, 128], [75, 75]),
                        ([0, 255, 255], [90, 90]),
                        ([0, 128, 255], [105, 105]),
                        ([0, 0, 255], [120, 120])]:
    boxes.append(UpDownBox(color, location))

screen = pygame.display.set_mode([150, 150])
while pygame.event.poll().type != KEYDOWN:
    screen.fill([0, 0, 0]) # blank the screen.

    # Save time by only calling this once
    time = pygame.time.get_ticks() 
    for b in boxes:
      b.update(time, 150)
      screen.blit(b.image, b.rect)

    pygame.display.update()
