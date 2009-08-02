import pygame
from pygame.locals import *

from foreverdrive.base import ForeverMain, Mode, PAUSE
from foreverdrive.sprite import Sprite
from foreverdrive.area import BoundArea

def report(*args, **kwargs):
    print "args:", args
    print "kwargs:", kwargs

class TestMode(Mode):

    def __init__(self, *args, **kwargs):
        super(TestMode, self).__init__(*args, **kwargs)
        self.area = BoundArea("default_tile.png",
                              size=(5, 10),
                              initial_position=(125, 125))
        self.groups.append(self.area)

    def first_entering(self):
        super(TestMode, self).entering()

        self.new = False
        self.game.groups.append(self.area)

        sprite = Sprite()
        self.game.listen_arrows(sprite.handle_event)
        self.game.listen_arrows(report)
            
        self.area.add(sprite)

def main():
    game = ForeverMain(initmode=TestMode)

    game.run()

if __name__ == "__main__":
    main()
