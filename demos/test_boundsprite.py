import pygame
from pygame.locals import *
from pygame import Surface, Color
from pygame.sprite import Sprite

from foreverdrive.base import ForeverMain
from foreverdrive.area import TileArea
from foreverdrive.sprite.bound import BoundSprite

def main():
    game = ForeverMain()

    group = pygame.sprite.RenderUpdates()
    background = BoundSprite()
    background.image = Surface((500, 500))
    group.add(background)

    sprite = BoundSprite()
    sprite.image = Surface((50, 50))
    sprite.image.fill(Color(200, 100, 100))
    group.add(sprite)

    game.groups.append(group)

    sprite.register_listeners(game.mode)

    game.run()

if __name__ == "__main__":
    main()
