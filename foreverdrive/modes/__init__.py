import pygame
from pygame.locals import *

from foreverdrive.events import EventRouter
from foreverdrive.area import BlurredBackground
from foreverdrive.events import Pause

class Mode(EventRouter):
    def __init__(self, game):
        super(Mode, self).__init__()
        self.game = game
        self.background = BlurredBackground("default_tile.png",
                                   (10, 10))

        self.groups = []

    def first_entering(self):
        pass

    new = True
    def entering(self):
        if self.new:
            self.new = False
            self.first_entering()
        for group in self.groups:
            for sprite in group:
                try:
                    handle_event = sprite.handle_event
                except AttributeError:
                    pass
                else:
                    handle_event(Pause())

    def leaving(self):
        pass

class InitialMode(Mode):

    def __init__(self, game):
        super(InitialMode, self).__init__(game)
        self.listen(self.enter_pause, KEYUP, K_p)

    def enter_pause(self, event):
        self.route(PAUSE)
        self.game.set_mode('pause')



class PauseMode(Mode):

    def __init__(self, game):
        super(PauseMode, self).__init__(game)
        self.listen(self.leave_pause, KEYUP, K_p)

    def leave_pause(self, event):
        self.game.set_mode('init')
