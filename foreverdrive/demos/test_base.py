import pygame
from pygame.locals import *

from foreverdrive.base import ForeverMain
from foreverdrive.shapes import MovingBox

def main():
    game = ForeverMain()
    box = MovingBox((128, 64, 196), (200, 200))
    for event_type in (KEYUP, KEYDOWN):
        for event_key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
            game.events.listen(box.handle_event, event_type, event_key)
    boxes = pygame.sprite.RenderUpdates()
    boxes.add(box)
    game.groups.append(boxes)
    game.run()

if __name__ == "__main__":
    main()
