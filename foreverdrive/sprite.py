import pygame
from pygame.locals import *

from foreverdrive import get_media_path
from foreverdrive.events import Pause, Movement

class Bound(object):
    def __init__(self, sprite):
        self.sprite = sprite
    @property
    def rect(self):
        return self.sprite.boundrect

class Sprite(pygame.sprite.Sprite):

    hmove = 0
    vmove = 0
    lastmove = 0
    speed = 2.0
    speed_multiplier = 2

    def __init__(self,
                 topleft=(100, 100),
                 bound_topleft=None,
                 image_path="default_sprite.png",
                 area=None):

        # All sprite classes should extend pygame.sprite.Sprite. This
        # gives you several important internal methods that you probably
        # don't need or want to write yourself. Even if you do rewrite
        # the internal methods, you should extend Sprite, so things like
        # isinstance(obj, pygame.sprite.Sprite) return true on it.
        pygame.sprite.Sprite.__init__(self)
        self.area = area
      
        # Create the image that will be displayed and fill it with the
        # right color.
        self.image = pygame.image.load(get_media_path(image_path)).convert_alpha()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = topleft

        if bound_topleft is None:
            bound_top = self.rect.height - 1
            bound_left = 0
        else:
            bound_top, bound_left = bound_topleft
        self.bound_top = bound_top
        self.bound_left = bound_left

        self.boundrect = pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.rect.width,
            1)

        self.adjust_inside_area()

        self.boundtop += self.rect.height - bound_top
        self.boundleft -= bound_left

    def adjust_inside_area(self):
        try:
            self.boundtop += self.area.top
            self.boundleft += self.area.left
        except AttributeError:
            pass

    @property
    def bound(self):
        return Bound(self)

    @property
    def boundtop(self):
        return self.boundrect.top
    @boundtop.setter
    def boundtop(self, top):
        self.boundrect.top = top
        self.rect.top = top

    @property
    def boundleft(self):
        return self.boundrect.left
    @boundleft.setter
    def boundleft(self, left):
        self.boundrect.left = left
        self.rect.left = left
        

    def update(self, current_time):
        if current_time == self.lastmove and self.lastmove > 0:
            return
        speed = self.speed
        self.boundrect.top += self.vmove * speed
        self.boundrect.left += self.hmove * speed
        self.rect.top += self.vmove * speed
        self.rect.left += self.hmove * speed

        if self.vmove or self.hmove:
            self.announce_movement()
        self.lastmove = current_time

    game = None
    def announce_movement(self):
        if self.game is not None:
            self.game.mode.route(Movement(self, (self.hmove, self.vmove)))

    def register_listeners(self, router):
        router.listen_arrows(self.handle_event)
        router.listen(self.handle_event, KEYDOWN, K_RSHIFT)
        router.listen(self.handle_event, KEYUP, K_RSHIFT)

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

        elif event.key == pygame.locals.K_RSHIFT and event.type == pygame.locals.KEYDOWN:
            self.speed *= self.speed_multiplier
        elif event.key == pygame.locals.K_RSHIFT and event.type == pygame.locals.KEYUP:
            self.speed = type(self).speed

class FacingSprite(Sprite):

    def __init__(self, *args, **kwargs):
        imagename = kwargs.pop('imagename')
        kwargs['image_path'] = "%s_down.png" % (imagename,)
        super(FacingSprite, self).__init__(*args, **kwargs)

        self.image_down = self.image
        self.image_up = pygame.image.load(get_media_path(imagename + "_up.png")).convert_alpha()
        self.image_right = pygame.image.load(get_media_path(imagename + "_right.png")).convert_alpha()
        self.image_left = pygame.image.load(get_media_path(imagename + "_left.png")).convert_alpha()

    def update(self, current_time):
        super(FacingSprite, self).update(current_time)
        if self.hmove > 0:
            self.image = self.image_right
        elif self.hmove < 0:
            self.image = self.image_left

        if self.vmove > 0:
            self.image = self.image_down
        elif self.vmove < 0:
            self.image = self.image_up
        
        
