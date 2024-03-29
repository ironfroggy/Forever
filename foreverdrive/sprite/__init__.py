from random import randint
from math import ceil, floor

import pygame
from pygame.locals import *

from foreverdrive import get_media_path
from foreverdrive.events import Pause, Movement, EventRouter, Entering
from foreverdrive.sprite.util import Bound, RectHolder
from foreverdrive.media import Media, default_spriteset

media_manager = Media()

class Sprite(pygame.sprite.Sprite):

    last_hv = (0, 0)
    hmove = 0
    vmove = 0
    lastmove = 0
    speed = 4.0
    speed_multiplier = 2.5
    z_sub = 0

    pushedby = None

    def __init__(self,
                 topleft=(100, 100),
                 image_path="default_sprite",
                 area=None,
                 height=None,
                 name=None,
                 *args, **kwargs):

        self.spriteset = kwargs.pop('spriteset', default_spriteset)
        self.slotgroup = kwargs.pop('slotgroup', "defaults")
        self.slotname = kwargs.pop('slotname', "tile")

        # All sprite classes should extend pygame.sprite.Sprite. This
        # gives you several important internal methods that you probably
        # don't need or want to write yourself. Even if you do rewrite
        # the internal methods, you should extend Sprite, so things like
        # isinstance(obj, pygame.sprite.Sprite) return true on it.
        pygame.sprite.Sprite.__init__(self)
        self.area = area
        self.name = name
        self.children = set()
      
        # Create the image that will be displayed and fill it with the
        # right color.
        self.image = self.spriteset.load(self.slotgroup, self.slotname)

        self.height = height or self.image.get_height()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        top, left = topleft

        self.boundrect = pygame.Rect(
            0,
            0,
            self.rect.width,
            self.height)

        self.rect.top -= self.rect.height - self.height
        self.boundtop = top
        self.boundleft = left

        self.width = self.rect.width
        self.lastmovebound = RectHolder(self.boundrect)

        self.adjust_inside_area()

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
        top_offset = top - self.boundrect.top
        self.boundrect.top += top_offset
        try:
            self.z = self.parent.z
        except AttributeError:
            self.z = z = self.rect.top + self.rect.height
        self.rect.top += top_offset
        for child in self.children:
            child.rect.top += top_offset

    @property
    def boundleft(self):
        return self.boundrect.left
    @boundleft.setter
    def boundleft(self, left):
        left_offset = left - self.boundrect.left
        self.boundrect.left += left_offset
        self.rect.left += left_offset
        for child in self.children:
            child.rect.left += left_offset

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

            self.boundtop += vmove
            self.boundleft += hmove

            if not self.area.keep_inside(self):
                self.last_hv = (hmove, vmove)
                self.area.mode.route(Movement(self, (hmove, vmove)))

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


    def grow_part(self, (top, left), partname):
        image = pygame.image.load(media_manager.open('sprite', 'defaults', 'default', partname)).convert_alpha()

        part_sprite = pygame.sprite.Sprite()
        part_sprite.image = image
        part_sprite.rect = image.get_rect()
        self.children.add(part_sprite)
        self.area.add(part_sprite)
        part_sprite.parent = self
        part_sprite.z_sub = self.z_sub + 1

        part_sprite.rect.top = self.rect.top + top
        part_sprite.rect.left = self.rect.left + left
        
class PerimeterSensoringMixin(EventRouter):
    """Mixin for sprites to watch other things in their area
    and trigger an event when things enter and leave their
    bounds.
    """

    def __init__(self, *args, **kwargs):
        super(PerimeterSensoringMixin, self).__init__(*args, **kwargs)

        self.sprites_inside = set()

    def check_collisions(self, area):
        try:
            self.__checking_collisions
        except AttributeError:
            self.__checking_collisions = 0

        try:
            self.__checking_collisions += 1
            hit = []
            for entered_portal in pygame.sprite.spritecollide(
                Bound(self),
                [Bound(s) for s in area if isinstance(s, PerimeterSensoringMixin)],
                False):

                if entered_portal.sprite is self:
                    continue
                entered_portal.on_overlap(area, self)
                hit.append(entered_portal)
            return hit
        finally:
            self.__checking_collisions -= 1

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
            P = 3.0
        else:
            try:
                P = min(sprite.pressure, self.pressure)
            except AttributeError:
                return

        sx, sy, sh, sw = self._get_pushing_bound(sprite)

        ox = sprite.boundleft
        oy = sprite.boundtop
        oh = sprite.height
        ow = sprite.width

        dx1 = sx + ow - ox
        dx2 = ox + ow - sx
        dx = (dx2, -dx1)[abs(dx1) < abs(dx2)] / 2.0 * P

        dy1 = sy + sh - oy
        dy2 = oy + oh - sy
        dy = (dy2, -dy1)[abs(dy1) < abs(dy2)] / 2.0 * P

        self._push_apart_xy(sprite, dx, dy)

        self.sprites_inside.remove(sprite)
        self.pushedby = sprite

    def _push_apart_xy(self, sprite, dx, dy):
        lx, ly = sprite.last_hv
        cx, cy = sprite.hmove, sprite.vmove

        mx = dx
        my = dy

        # Move on the shortest axis
        # Which is also the direction the pusher is moving
        if abs(dx) < abs(dy) and (lx or not ly or cx):
            self.move(x=mx)
        elif abs(dx) > abs(dy) and (ly or not lx or cy):
            self.move(y=my)
        else:
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
    def _push_apart_xy(self, sprite, dx, dy):
        lx, ly = sprite.last_hv
        cx, cy = sprite.hmove, sprite.vmove

        mx = dx
        my = dy

        # Move on the shortest axis
        # Which is also the direction the pusher is moving
        if abs(dx) < abs(dy) and (lx or not ly or cx):
            sprite.hmove = 0
        elif abs(dx) > abs(dy) and (ly or not lx or cy):
            sprite.vmove = 0


class CloudSprite(SolidSprite):

    radius = 25
    turbulance = (100, 20)

    def check_overlap(self, sprite):
        """Cloud-like things aren't rectangles!"""
        return pygame.sprite.collide_circle(Bound(self), Bound(sprite))

    def _get_pushing_bound(self, sprite):
        x = 0
        y = 0
        c, t = self.turbulance
        if randint(0, 100) < c:
            x = randint(-t, t)
            y = randint(-t, t)
            self.boundtop += y
            self.boundleft += x
        return self.boundleft, self.boundtop, self.height, self.width


class FacingSprite(Sprite):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('slotgroup', 'body')
        super(FacingSprite, self).__init__(*args, **kwargs)

        slotgroup = self.slotgroup
        self.image_down = self.spriteset.load(slotgroup, 'down')
        self.image_up = self.spriteset.load(slotgroup, 'up')
        self.image_left = self.spriteset.load(slotgroup, 'left')
        self.image_right = self.spriteset.load(slotgroup, 'right')

    def update(self, current_time):
        speed = self.speed
        super(FacingSprite, self).update(current_time)
        self.speed = speed

        main = self
        while True:
            try:
                main = main.parent
            except AttributeError:
                break

        if main.hmove > 0:
            self.image = self.image_right
        elif main.hmove < 0:
            self.image = self.image_left

        if main.vmove > 0:
            self.image = self.image_down
        elif main.vmove < 0:
            self.image = self.image_up

    def grow_part(self, (top, left), partname):
        part_sprite = FacingSprite(spriteset=self.spriteset, slotgroup=partname)

        part_sprite.rect = part_sprite.image.get_rect()
        self.children.add(part_sprite)
        self.area.add(part_sprite)

        part_sprite.rect.top = self.rect.top + top
        part_sprite.rect.left = self.rect.left + left

        part_sprite.parent = self
        part_sprite.z_sub = self.z_sub + 1


class Player(FacingSprite, SolidSprite):
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
