import pygame
from pygame.locals import *

from foreverdrive import get_media_path
from foreverdrive.events import Pause, Movement

class Sprite(pygame.sprite.Sprite):

    hmove = 0
    vmove = 0
    lastmove = 0
    speed = 10.0

    def __init__(self, topleft=(100, 100), image_path="default_sprite.png"):

        # All sprite classes should extend pygame.sprite.Sprite. This
        # gives you several important internal methods that you probably
        # don't need or want to write yourself. Even if you do rewrite
        # the internal methods, you should extend Sprite, so things like
        # isinstance(obj, pygame.sprite.Sprite) return true on it.
        pygame.sprite.Sprite.__init__(self)
      
        # Create the image that will be displayed and fill it with the
        # right color.
        self.image = pygame.image.load(get_media_path(image_path)).convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = topleft

        self.boundrect = pygame.Rect(self.rect.left,
                                     self.rect.top + self.rect.height - 1,
                                     self.rect.width,
                                     1)

    @property
    def boundtop(self):
        return self.boundrect.top
    @boundtop.setter
    def boundtop(self, top):
        self.boundrect.top = top
        self.rect.top = top - self.rect.height
        

    def update(self, current_time):
        self.boundrect.top += self.vmove
        self.boundrect.left += self.hmove
        self.rect.top += self.vmove
        self.rect.left += self.hmove

        if self.vmove or self.hmove:
            self.announce_movement()
        self.lastmove = current_time

    game = None
    def announce_movement(self):
        if self.game is not None:
            self.game.mode.route(Movement(self, (self.hmove, self.vmove)))

    def handle_event(self, event):
        if isinstance(event, Pause):
            self.hmove = 0
            self.vmove = 0
            return

        if event.type == pygame.locals.KEYDOWN:
            change = 1
        elif event.type == pygame.locals.KEYUP:
            change = -1

        if event.key == pygame.locals.K_UP:
            self.vmove -= change
        elif event.key == pygame.locals.K_DOWN:
            self.vmove += change
        elif event.key == pygame.locals.K_LEFT:
            self.hmove -= change
        elif event.key == pygame.locals.K_RIGHT:
            self.hmove += change
