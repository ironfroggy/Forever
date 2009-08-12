from itertools import chain

import pygame
from foreverdrive import get_media_path
from foreverdrive.errors import PlacementError
from foreverdrive.events import Movement, CancelEvent
from foreverdrive.sprite import Sprite, Bound
from foreverdrive.sprite.portal import Portal
from foreverdrive.visual.filters import blur, dim


class TileArea(object):
    name = None
    filters = []

    def __init__(self,
                 spriteset,
                 size,
                 topleft=(0, 0),
                 mode=None):

        self.spriteset = spriteset
        self.mode = mode
        self.neighbors = set()

        self.image = spriteset.load("default", "tile")
        for filter in self.filters:
            filter(self.image)

        self.screen = pygame.display.get_surface()

        self._top, self._left = topleft
        self.width = self.image.get_width() * size[0]
        self.height = self.image.get_height() * size[1]

        tg = self.tile_group = pygame.sprite.OrderedUpdates()
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                sprite = pygame.sprite.Sprite()
                sprite.image = spriteset.load("default", "tile")
                sprite.rect = sprite.image.get_rect()
                sprite.rect.top = self._top + self.image.get_height() * y
                sprite.rect.left = self._left + self.image.get_width() * x
                tg.add(sprite)

        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect((self.left, self.top), (self.width, self.height))

    def __iter__(self):
        return iter(self.tile_group)

    # When top/left change, all sprites change
    @property
    def top(self):
        return self._top
    @top.setter
    def top(self, new_top):
        change = new_top - self._top
        self._top = new_top
        for sprite in self:
            sprite.rect.top += change
            try:
                sprite.boundrect.top += change
            except AttributeError:
                pass

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def left(self):
        return self._left
    @left.setter
    def left(self, new_left):
        change = new_left - self._left
        self._left = new_left
        for sprite in self:
            sprite.rect.left += change
            try:
                sprite.boundrect.left += change
            except AttributeError:
                pass
        self.update_rect()
    @property
    def right(self):
        return self.left + self.width

    @property
    def top_left(self):
        return (self.top, self.left)
    @property
    def top_right(self):
        return (self.top, self.right)
    @property
    def bottom_left(self):
        return (self.top + self.height, self.left)
    @property
    def bottom_right(self):
        return (self.top + self.height, self.left + self.width)

    def update_and_draw(self, ticks):
        self.update(ticks)
        return self.draw(self.screen)

    def update(self, ticks):
        self.tile_group.update(ticks)

    def get_groups(self):
        return [(10, self.tile_group)]

    def draw(self, screen):
        screen = self.screen
        return self.tile_group.draw(screen)

    def update(self, ticks):
        pass

    def create_sprite(self, cls, *args, **kwargs):
        kwargs['area'] = self
        kwargs.setdefault('spriteset', self.spriteset)
        sprite = cls(*args, **kwargs)
        self.add(sprite)
        sprite.mode = self.mode
        return sprite

class BlurredBackground(TileArea):
    filters = [blur, blur, blur, blur]

    scroll_rollover_top = 0
    scroll_rollover_left = 0

    parallax_multiplier = 0.8

    def on_scroll(self, event):
        p = self.parallax_multiplier
        top = event.y * p + self.scroll_rollover_top
        left = event.x * p + self.scroll_rollover_left

        if top >= 1 or top <= -1:
            self.top += int(top)
        self.scroll_rollover_top = top % 1

        if left >= 1 or left <= -1:
            self.left += int(left)
        self.scroll_rollover_left = left % 1


class BoundArea(TileArea):

    def __init__(self, *args, **kwargs):
        super(BoundArea, self).__init__(*args, **kwargs)
        self.bound_group = pygame.sprite.OrderedUpdates()
        if self.mode:
            self.mode.listen(self.on_movement, Movement)

    def __iter__(self):
        return chain(self.tile_group, self.bound_group)

    def add(self, sprite):
        self.bound_group.add(sprite)

    def remove(self, sprite):
        self.bound_group.remove(sprite)

    def _sprite_key(self, sprite):
        if getattr(sprite, 'pushedby', None) is None:
            return 0
        else:
            return self._sprite_key(sprite.pushedby) - 1

    def update(self, ticks):
        self.bound_group.update(ticks)
        for bound_sprite in self.bound_group:
            self.keep_inside(bound_sprite)
        for bound_sprite in chain(self.bound_group, *(n.bound_group for n in self.neighbors)):
            try:
                cc = bound_sprite.check_collisions
            except AttributeError:
                pass
            else:
                cc(self)

        def sprite_key(sprite):
            try:
                try:
                    return sprite.z + sprite.z_sub
                except:
                    return (sprite.boundtop, 0)
            except:
                return (sprite.rect.top, 0)

        group = self.bound_group
        sprites = list(group)
        sprites.sort(key=sprite_key)
        group.empty()
        group.add(sprites)

    def keep_inside(self, bound_sprite):
        try:
            rect = bound_sprite.boundrect
        except AttributeError:
            return

        topleft = bound_sprite.boundtop, bound_sprite.boundleft

        new_left = min(max(self.left, rect.left),
                      self.left + self.width - rect.width)
        new_top = min(max(self.top, rect.top),
                      self.top + self.height - rect.height)
        
        bound_sprite.boundtop = new_top
        bound_sprite.boundleft = new_left
        
        return topleft != (bound_sprite.boundtop, bound_sprite.boundleft)

    def on_movement(self, event):
        pass

    def draw(self, surface):
        return chain(
            super(BoundArea, self).draw(surface) +
            self.bound_group.draw(surface))

    def get_groups(self):
        return chain(super(BoundArea, self).get_groups(),
                [(50, self.bound_group)])
