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
        self.game.groups.append(self.area)

        sprite = FacingSprite(topleft=(self.area.top+50, self.area.left+50), imagename="default_player")
        sprite.register_listeners(self.game.mode)
        self.player = sprite
    
        self.area.add(sprite)
        super(TestMode, self).first_entering()

def main():
    game = ForeverMain(initmode=TestMode)

    game.run()

if __name__ == "__main__":
    main()
