import pygame
from pygame.locals import *
from pygame import Surface, Color

from foreverdrive.base import ForeverMain
from foreverdrive.area import TileArea
from foreverdrive.sprite.bound import BoundSprite

def main():
    game = ForeverMain()
    sprite = BoundSprite()
    sprite.image = Surface((100, 100))
    sprite.image.fill(Color(200, 100, 100))
    group = pygame.sprite.RenderUpdates()
    group.add(sprite)
    game.groups.append(group)

    sprite.velocity = (200.0, 100.0)

    game.run()

if __name__ == "__main__":
    main()
