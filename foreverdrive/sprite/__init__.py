from random import randint
from math import ceil, floor

import pygame
from pygame.locals import *

from foreverdrive import get_media_path
from foreverdrive.events import Pause, Movement, EventRouter, Entering, CancelEvent
from foreverdrive.sprite.util import Bound, RectHolder


class Sprite(pygame.sprite.Sprite):

    last_hv = (0, 0)
    hmove = 0
    vmove = 0
    lastmove = 0
    speed = 4.0
    speed_multiplier = 2.5

    pushedby = None

    def __init__(self,
                 topleft=(100, 100),
                 image_path="default_sprite.png",
                 area=None,
                 height=1,
                 name=None):

        # All sprite classes should extend pygame.sprite.Sprite. This
        # gives you several important internal methods that you probably
        # don't need or want to write yourself. Even if you do rewrite
        # the internal methods, you should extend Sprite, so things like
        # isinstance(obj, pygame.sprite.Sprite) return true on it.
        pygame.sprite.Sprite.__init__(self)
        self.area = area
        self.name = name
        self.height = height
      
        # Create the image that will be displayed and fill it with the
        # right color.
        self.image = pygame.image.load(get_media_path(image_path)).convert_alpha()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = topleft

        self.boundrect = pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.rect.width,
            height)
        self.width = self.rect.width
        self.lastmovebound = RectHolder(self.boundrect)

        self.adjust_inside_area()

        self.children = set()

    def __iter__(self):
        return iter(self.children)

    def show_bounds(self):
        sprite = RectShower(self.boundrect)
        self.area.add(sprite)
        self.children.add(sprite)

        #sprite = RectShower(self.rect, (50, 50, 50))
        #self.area.add(sprite)
        #self.children.add(sprite)

    def adjust_inside_area(self):
        try:
            self.boundtop += self.area.top - self.height
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
        diff = top - self.boundrect.top
        self.boundrect.top = top + diff
        self.rect.top = top - diff

    @property
    def boundleft(self):
        return self.boundrect.left
    @boundleft.setter
    def boundleft(self, left):
        diff = left - self.boundrect.left
        self.boundrect.left = left + diff
        self.rect.left = left - diff
        

    def update(self, current_time):
        if current_time == self.lastmove and self.lastmove > 0:
            return False

        self.move()
        self.lastmove = current_time

        for child in self:
            child.update(current_time)

        return True

    def pushedby_all(self):
        if self.pushedby is not None:
            return [self.pushedby] + self.pushedby.pushedby_all()
        else:
            return []

    def move(self, M=1, x=None, y=None):
        speed = self.speed * M
        vmove = self.vmove * speed if y is None else y
        hmove = self.hmove * speed if x is None else x

        previous_top = self.boundtop
        previous_left = self.boundleft

        if vmove or hmove:
            #print self.name, (hmove, vmove), self.speed,
            last_lastmovebound = RectHolder(pygame.Rect(
                    self.boundrect.left,
                    self.boundrect.top,
                    self.boundrect.width,
                    self.boundrect.height))

            self.boundrect.top += vmove
            self.boundrect.left += hmove
            #print self.boundrect
            self.rect.top += vmove
            self.rect.left += hmove

            self.last_hv = (hmove, vmove)
            self.lastmovebound = RectHolder(pygame.Rect(
                    self.boundrect.left - hmove,
                    self.boundrect.top - vmove,
                    self.boundrect.width + abs(hmove),
                    self.boundrect.height + abs(vmove)
                    ))
            try:
                self.announce_movement(hmove, vmove)
            except CancelEvent:
#                print "  couldn't move."
                self.boundtop = previous_top - vmove
                self.boundleft = previous_left - hmove
                self.lastmovebound = last_lastmovebound

    mode = None
    def announce_movement(self, hmove, vmove):
        if self.mode is not None:
            self.mode.route(Movement(self, (hmove, vmove)))
            

    def register_listeners(self, router):
        router.listen_arrows(self.handle_event)
        router.listen(self.handle_event, KEYDOWN, K_RSHIFT)
        router.listen(self.handle_event, KEYUP, K_RSHIFT)
        router.listen(self.handle_event, KEYDOWN, K_LSHIFT)
        router.listen(self.handle_event, KEYUP, K_LSHIFT)

    def handle_event(self, event):
        if isinstance(event, Pause):
            self.hmove = 0
            self.vmove = 0
            return

        if event.type in (KEYDOWN, KEYUP):
            go = int(event.type == KEYDOWN)

            if event.key == K_UP:
                self.vmove = -go
            elif event.key == K_DOWN:
                self.vmove = go
            elif event.key == K_LEFT:
                self.hmove = -go
            elif event.key == K_RIGHT:
                self.hmove = go

        if event.key == pygame.locals.K_RSHIFT and event.type == pygame.locals.KEYDOWN:
            self.speed *= self.speed_multiplier
        elif event.key == pygame.locals.K_RSHIFT and event.type == pygame.locals.KEYUP:
            self.speed = type(self).speed

        elif event.key == pygame.locals.K_LSHIFT and event.type == pygame.locals.KEYDOWN:
            self.speed = 1
        elif event.key == pygame.locals.K_LSHIFT and event.type == pygame.locals.KEYUP:
            self.speed = type(self).speed

        print self.speed

#        if self.hmove or self.vmove:
#            print "player moved", (self.hmove, self.vmove)
        
class PerimeterSensoringMixin(EventRouter):
    """Mixin for sprites to watch other things in their area
    and trigger an event when things enter and leave their
    bounds.
    """

    def __init__(self, *args, **kwargs):
        super(PerimeterSensoringMixin, self).__init__(*args, **kwargs)
        
        self.area.portals.add(self)
        self.sprites_inside = set()

    def check_overlap(self, sprite):
        return pygame.sprite.collide_rect(Bound(self), Bound(sprite))

    def on_overlap(self, area, sprite):
        """`sprite` is in the bounds of `self`."""

        if sprite in self.sprites_inside:
            if self.check_overlap(sprite):
                return self.on_stillin(area, sprite)
            else:
                self.sprites_inside.remove(sprite)
                return self.on_leave(area, sprite)

        if not self.check_overlap(sprite):
            return False
        else:
            self.sprites_inside.add(sprite)
            return self.on_enter(area, sprite)

    def on_enter(self, area, sprite):
        pass

    def on_leave(self, area, sprite):
        pass

    def on_stillin(self, area, sprite):
        pass

class SolidSprite(PerimeterSensoringMixin, Sprite):

    hmove = 0
    vmove = 0

    pressure = 1.0

    def __init__(self, *args, **kwargs):
        self.can_move = kwargs.pop('can_move', (1, 1, 1, 1))
        super(SolidSprite, self).__init__(*args, **kwargs)

    def _get_pushing_bound(self, sprite):
        return self.boundleft, self.boundtop, self.height, self.width

    def push_apart(self, sprite):
        if isinstance(sprite, ImmovableSprite):
            P = 1.0
        else:
            P = min(sprite.pressure, self.pressure)

        sx, sy, sh, sw = self._get_pushing_bound(sprite)

        ox = sprite.boundleft
        oy = sprite.boundtop
        oh = sprite.height
        ow = sprite.width

        dx1 = sx + ow - ox
        dx2 = ox + ow - sx
        dx = (dx2, -dx1)[abs(dx1) < abs(dx2)] / 2.0 * P

        dy1 = sy + sh - oy
        dy2 = oy + sh - sy
        dy = (dy2, -dy1)[abs(dy1) < abs(dy2)] / 2.0 * P

        self._push_apart_xy(sprite, dx, dy)

        self.sprites_inside.remove(sprite)
        self.pushedby = sprite

    def _push_apart_xy(self, sprite, dx, dy):
        lx, ly = sprite.last_hv
        cx, cy = sprite.hmove, sprite.vmove

        mx = (floor(dx+1) if dx > 0 else ceil(dx)-1)
        my = (floor(dy+1) if dy > 0 else ceil(dy)-1)

        # Move on the shortest axis
        # Which is also the direction the pusher is moving
        if abs(dx) < abs(dy) and (lx or not ly or cx):
            self.move(x=mx)
        elif abs(dx) > abs(dy) and (ly or not lx or cy):
            self.move(y=my)

        self.move(x=randint(-1, 1), y=randint(-1, 1))

    def update(self, tick):
        sprites_inside = list(self.sprites_inside)
        for sprite in sprites_inside:
            self.push_apart(sprite)

        if not super(SolidSprite, self).update(tick):
            return False

        self.speed = (self.speed + type(self).speed) * 0.95
        self.pushedby = None


class ImmovableSprite(SolidSprite):
    def push_apart(self, sprite):
        return


class CloudSprite(SolidSprite):

    radius = 25
    def check_overlap(self, sprite):
        """Cloud-like things aren't rectangles!"""
        return pygame.sprite.collide_circle(Bound(self), Bound(sprite))


class FacingSprite(SolidSprite):

    def __init__(self, *args, **kwargs):
        imagename = kwargs.pop('imagename')
        kwargs['image_path'] = "%s_down.png" % (imagename,)
        super(FacingSprite, self).__init__(*args, **kwargs)

        self.image_down = self.image
        self.image_up = pygame.image.load(get_media_path(imagename + "_up.png")).convert_alpha()
        self.image_right = pygame.image.load(get_media_path(imagename + "_right.png")).convert_alpha()
        self.image_left = pygame.image.load(get_media_path(imagename + "_left.png")).convert_alpha()

    def update(self, current_time):
        speed = self.speed
        super(FacingSprite, self).update(current_time)
        self.speed = speed

        if self.hmove > 0:
            self.image = self.image_right
        elif self.hmove < 0:
            self.image = self.image_left

        if self.vmove > 0:
            self.image = self.image_down
        elif self.vmove < 0:
            self.image = self.image_up


class RectShower(pygame.sprite.Sprite):
    def __init__(self, show_for, color=(128, 128, 128)):
        super(RectShower, self).__init__()
        self.color = color
        self.image = pygame.Surface((show_for.width,
                                       show_for.height))
        self.show_for = show_for
        self.update(0)

    def update(self, update_time):
        show_for = self.show_for
        image = self.image

        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.top = show_for.top
        self.rect.left = show_for.left
