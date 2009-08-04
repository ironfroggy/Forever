from math import ceil, floor

import pygame
from pygame.locals import *

from foreverdrive import get_media_path
from foreverdrive.events import Pause, Movement, EventRouter, Entering, CancelEvent

class Bound(object):
    def __init__(self, sprite):
        self.sprite = sprite
    @property
    def rect(self):
        return self.sprite.boundrect

    def __getattr__(self, name):
        return getattr(self.sprite, name)

class RectHolder(object):
    def __init__(self, rect):
        self.rect = rect


class BoundSprite(pygame.sprite.Sprite):

    def __init__(self, bound_to, down_right):
        self.bound_to = to
        self.bound_offset = down_right

    def update(self, ticks):
        bound_to = self.bound_to.rect
        down, right = self.bound_offset
        self.rect.top = bound_to.top + down
        self.rect.left = bound_to.left + right


class MovingSpriteMixin(object):
    """Anything that can be in motion will use this to
    """

    def __init__(self, *args, **kwargs):
        pass 


class Sprite(pygame.sprite.Sprite):

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
#        diff = self.boundrect.top - self.rect.top
        self.boundrect.top = top# + diff
        self.rect.top = top# - diff

    @property
    def boundleft(self):
        return self.boundrect.left
    @boundleft.setter
    def boundleft(self, left):
        self.boundrect.left = left
        self.rect.left = left
        

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

    def enter(self, area, sprite):
        if sprite in self.sprites_inside:
            if pygame.sprite.collide_rect(Bound(self), Bound(sprite)):
                #print sprite.name, "still in", self.name, (sprite.boundrect, self.boundrect)
                return False
            else:
                #print sprite.name, "leaving", self.name
                self.sprites_inside.remove(sprite)
                return False

        if not pygame.sprite.collide_rect(Bound(self), Bound(sprite)):
            return False
        else:
            self.sprites_inside.add(sprite)
            #print sprite.name, "entering", self.name, (sprite.boundrect, self.boundrect)
            self.route(Entering(sprite, self))
            return True

class SolidSprite(PerimeterSensoringMixin, Sprite):

    hmove = 0
    vmove = 0

    def __init__(self, *args, **kwargs):
        self.can_move = kwargs.pop('can_move', (1, 1, 1, 1))
        super(SolidSprite, self).__init__(*args, **kwargs)

    def push_apart(self, sprite):
        sx = self.boundleft
        sy = self.boundtop
        sh = self.height
        sw = self.width

        ox = sprite.boundleft
        oy = sprite.boundtop
        oh = sprite.height
        ow = sprite.width

        dx1 = sx + ow - ox
        dx2 = ox + ow - sx
        dx = (dx2, -dx1)[abs(dx1) < abs(dx2)] / 2.0

        dy1 = sy + sh - oy
        dy2 = oy + sh - sy
        dy = (dy2, -dy1)[abs(dy1) < abs(dy2)] / 2.0

        if dx < dy:
            #print "x", dx
            self.move(x=(floor(dx+1) if dx > 0 else ceil(dx)-1))
            #sprite.move(x=(floor(dx) if dx < 0 else ceil(dx))+1)
        elif dx > dy:
            #print "y", dy
            self.move(y=(floor(dy+1) if dy > 0 else ceil(dy)-1))
            #sprite.move(floor(-dy))
        self.sprites_inside.remove(sprite)

    def update(self, tick):
        for sprite in list(self.sprites_inside):
            self.push_apart(sprite)

        if not super(SolidSprite, self).update(tick):
            return False

        self.speed = type(self).speed
        self.pushedby = None
        self.slow_down()

    def slow_down(self):
        if self.vmove:
            self.vmove = 0
        if self.hmove:
            self.hmove = 0


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
        super(FacingSprite, self).update(current_time)

        if self.hmove > 0:
            self.image = self.image_right
        elif self.hmove < 0:
            self.image = self.image_left

        if self.vmove > 0:
            self.image = self.image_down
        elif self.vmove < 0:
            self.image = self.image_up

    def slow_down(self):
        pass


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
