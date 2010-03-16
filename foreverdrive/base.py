from collections import defaultdict

import pygame
from pygame.locals import *

from foreverdrive.area import TileArea
from foreverdrive.events import Movement, Scroll, EventRouter, Pause
from foreverdrive.modes import Mode, InitialMode, PauseMode

class Window(object):
    rect = pygame.Rect(100, 100, 300, 300)

class ForeverMain(object):
    """The ForeverMain instance represents the active game
    state. This manages the background, sprites, input,
    etc.
    """

    delay = 50

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

    def tick(self, tick):
        pass

    def run(self):
        pygame.init()
        screen = self.screen
        quit = False
        lastupdate = 0
        delay = self.delay
        while not quit:
            self.tick(lastupdate)
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
            drawlist = []
            update = ticks - lastupdate > delay
            ticks_passed = ticks - lastupdate
            if update:
                lastupdate = ticks
                mode.update(ticks_passed)
            for group in mode.groups:
                if update:
                    group.update(ticks_passed)
                try:
                    drawlist.extend(group.get_groups())
                except AttributeError:
                    drawlist.append((0, group))
            drawlist.sort()
            for (order, group) in drawlist:
                rectlist.extend(group.draw(screen))
            pygame.display.update(rectlist)
