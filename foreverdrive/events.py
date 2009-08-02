import pygame
from pygame.locals import *


class Movement(object):
    def __init__(self, player, movement):
        self.player = player
        self.rect = player.rect
        self.movement = movement

class Entering(object):
    def __init__(self, sprite, entered):
        self.sprite = sprite
        self.entered = entered

class Scroll(object):
    def __init__(self, window, movement):
        self.window = window
        self.x, self.y = movement

class Pause(object):
    pass

class EventRouter(object):
    def __init__(self, *args, **kwargs):
        super(EventRouter, self).__init__(*args, **kwargs)
        self.listeners = {}

    def listen(self, callback, *args, **kwargs):
        if len(args) == 1 and type(args[0]) is type:
            key = args[0]
        elif len(args) == 2:
            key = args

        self.listeners.setdefault(key, []).append(callback)

    def listen_arrows(self, callback):
        for event_type in (KEYUP, KEYDOWN):
            for event_key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                self.listen(callback, event_type, event_key)

    def route(self, event):
        if hasattr(event, 'type') and hasattr(event, 'key'):
            key = (event.type, event.key)
        else:
            key = type(event)

        for callback in self.listeners.get(key, []):
            callback(event)

