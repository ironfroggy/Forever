from collections import defaultdict

import pygame
from pygame.locals import *

from foreverdrive.area import TileArea

class EventRouter(object):
    def __init__(self):
        self.listeners = {}

    def listen(self, callback, type, key):
        self.listeners.setdefault((type, key), []).append(callback)

    def listen_arrows(self, callback):
        for event_type in (KEYUP, KEYDOWN):
            for event_key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                self.listen(callback, event_type, event_key)

    def route(self, event):
        if hasattr(event, 'type') and hasattr(event, 'key'):
            for callback in self.listeners.get((event.type, event.key), []):
                callback(event)

class ForeverMain(EventRouter):
    """The ForeverMain instance represents the active game
    state. This manages the background, sprites, input,
    etc.
    """

    def __init__(self):
        super(ForeverMain, self).__init__()
        self.screen = pygame.display.set_mode((500, 500))
        self.background = TileArea("default_tile.png",
                                   (10, 10))

        self.groups = []

    def run(self):
        pygame.init()
        screen = self.screen
        quit = False
        while not quit:
            ticks = pygame.time.get_ticks()
            background = self.background

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
                    self.route(event)

            rectlist = []
            rectlist.extend(background.update_and_draw(ticks))
            for group in self.groups:
                group.update(ticks)
                rectlist.extend(group.draw(screen))
            pygame.display.update(rectlist)
