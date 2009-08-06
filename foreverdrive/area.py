from itertools import chain

import pygame
from foreverdrive import get_media_path
from foreverdrive.events import Movement, CancelEvent
from foreverdrive.sprite import Sprite, Bound
from foreverdrive.visual.filters import blur, dim

class TileArea(object):
    name = None
    filters = []

    def __init__(self,
                 image_path,
                 size,
                 topleft=(0, 0),
                 relative_to=None,
                 mode=None):

        self.mode = mode

        self.image = pygame.image.load(get_media_path(image_path)).convert()
        for filter in self.filters:
            filter(self.image)

        self.screen = pygame.display.get_surface()

        self._top, self._left = topleft
        if relative_to is not None:
            try:
                rel_top = relative_to.top
                rel_left = relative_to.left
            except AttributeError:
                rel_top, rel_left = relative_to
            self._top += rel_top
            self._left += rel_left
        self.width = self.image.get_width() * size[0]
        self.height = self.image.get_height() * size[1]

        tg = self.tile_group = pygame.sprite.OrderedUpdates()
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                sprite = pygame.sprite.Sprite()
                sprite.image = self.image
                sprite.rect = self.image.get_rect()
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
            t = sprite.rect.top
            sprite.rect.top += change
        self.update_rect()
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
        self.portals = pygame.sprite.Group()
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

class AreaManager(object):
    """Manages multiple areas and portals between them."""

    def __init__(self, mode):
        self.mode = mode
        self.areas = []
        self.namedareas = {}

    def add(self, area):
        self.areas.append(area)
        self.namedareas[area.name] = area
        self.mode.groups.extend(self.areas)
        area.manager = self

    def new_area(self,
                 (top, left),
                 (tiles_wide, tiles_tall),
                 relative_to=None,
                 ):
        area = BoundArea("default_tile.png",
                         size=(tiles_wide, tiles_tall),
                         topleft=(top, left),
                         relative_to=relative_to,
                         mode=self.mode)
        self.add(area)
        return area

    def new_areas(self, dimensions, relative_to=None):
        areas = []
        for (topleft, size, reltype, children) in dimensions:
            area = self.new_area(topleft, size, relative_to=getattr(relative_to, reltype or "top_left", None))
            areas.append(area)
            if children is not None:
                areas.extend(self.new_areas(children, relative_to=area))
        return areas
