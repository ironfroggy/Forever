import pygame
from pygame.locals import *

from foreverdrive.base import ForeverMain
from foreverdrive.sprite import Sprite

def main():
    game = ForeverMain()
    sprite = Sprite()
    game.listen_arrows(sprite.handle_event)
    group = pygame.sprite.RenderUpdates()
    group.add(sprite)
    game.groups.append(group)
    game.run()

if __name__ == "__main__":
    main()
