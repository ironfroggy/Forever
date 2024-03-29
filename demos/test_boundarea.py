import pygame
from pygame.locals import *

from foreverdrive.base import ForeverMain, Mode
from foreverdrive.sprite import FacingSprite
from foreverdrive.area import BoundArea

def report(*args, **kwargs):
    print "args:", args
    print "kwargs:", kwargs

class TestMode(Mode):

    area_size = (5, 10)

    def __init__(self, *args, **kwargs):
        super(TestMode, self).__init__(*args, **kwargs)
        self.area = BoundArea("default_tile.png",
                              size=self.area_size,
                              topleft=(125, 125))
        self.groups.append(self.area)

    def first_entering(self):
        self.new = False
        self.game.groups.extend(self.areas)

        sprite = FacingSprite(topleft=(self.areas[0].top+50, self.areas[0].left+50), imagename="default_player")
        sprite.register_listeners(self.game.mode)
        self.player = sprite
    
        self.areas[0].add(sprite)
        super(TestMode, self).first_entering()

def main():
    game = ForeverMain(initmode=TestMode)

    game.run()

if __name__ == "__main__":
    main()
