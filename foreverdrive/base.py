from collections import defaultdict

import pygame
from pygame.locals import *

from foreverdrive.area import TileArea
from foreverdrive.events import Movement, Scroll

PAUSE = object()

class Window(object):
    rect = pygame.Rect(100, 100, 300, 300)

class Mode(EventRouter):
    def __init__(self, game):
        super(Mode, self).__init__()
        self.game = game
        self.background = TileArea("default_tile.png",
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
                    handle_event(PAUSE)

    def leaving(self):
        pass

class InitialMode(Mode):

    def __init__(self, game):
        super(InitialMode, self).__init__(game)
        self.listen(self.enter_pause, KEYUP, K_p)

    def enter_pause(self, event):
        self.route(PAUSE)
        self.game.set_mode('pause')

class ScrollingMode(Mode):

    def first_entering(self):
        super(ScrollingMode, self).first_entering()

        self.player.game = self.game
        self.listen_move(self.player_moved)

    def player_moved(self, event):
        rect = event.rect
        window = Window()

        x = 0
        y = 0

        bottom_over = (rect.top + rect.height) - (window.rect.top + window.rect.height)
        if bottom_over > 0:
            self.area.top -= bottom_over
            y = -bottom_over
        else:
            top_under = window.rect.top - rect.top
            if top_under > 0:
                self.area.top += top_under
                y = top_under

        right_over = (rect.left + rect.width) - (window.rect.left + window.rect.width)
        if right_over > 0:
            self.area.left -= right_over
            x = -right_over
        else:
            left_under = window.rect.left - rect.left
            if left_under > 0:
                self.area.left += left_under
                x = left_under

        if x or y:
            self.route(Scroll(window, (x, y)))


class PauseMode(Mode):

    def __init__(self, game):
        super(PauseMode, self).__init__(game)
        self.listen(self.leave_pause, KEYUP, K_p)

    def leave_pause(self, event):
        self.game.set_mode('init')

class ForeverMain(object):
    """The ForeverMain instance represents the active game
    state. This manages the background, sprites, input,
    etc.
    """

    def __init__(self, initmode=None):
        if initmode is None:
            initmode = InitialMode

        super(ForeverMain, self).__init__()
        self.screen = pygame.display.set_mode((500, 500))
        self.modes = {
            'init': initmode(self),
            'pause': PauseMode(self),
            }
        self.current_mode = 'init'
        self.mode.entering()

    def set_mode(self, modename):
        self.mode.leaving()
        self.current_mode = modename
        self.mode.entering()

    @property
    def mode(self):
        return self.modes[self.current_mode]
    @property
    def groups(self):
        return self.mode.groups

    def listen_arrows(self, *args, **kwargs):
        return self.mode.listen_arrows(*args, **kwargs)

    def run(self):
        pygame.init()
        screen = self.screen
        quit = False
        while not quit:
            mode = self.mode
            ticks = pygame.time.get_ticks()
            background = mode.background

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit = True
                    break
                elif event.type == KEYUP and event.key == K_ESCAPE:
                    quit = True
                    break
                elif event.type == KEYUP and event.key == K_F10:
                    import pdb
                    pdb.set_trace()
                else:
                    mode.route(event)

            rectlist = []
            rectlist.extend(background.update_and_draw(ticks))
            for group in mode.groups:
                group.update(ticks)
                rectlist.extend(group.draw(screen))
            pygame.display.update(rectlist)
