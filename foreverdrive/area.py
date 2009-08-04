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
        print mode

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

class Portal(Sprite):

    def __init__(self, *args, **kwargs):
        self.to = kwargs.pop('to', None)
        self.offset = kwargs.pop('offset', None)
        height = kwargs.pop('height', 100)
        width = kwargs.pop('width', 1)

        kwargs['image_path'] = "default_portal.png"
        super(Portal, self).__init__(*args, **kwargs)

        top, left = self.offset
        if left:
            self.rect.height = height
            self.rect.width = width

    def adjust_inside_area(self):
        self.rect.top += self.area.top
        self.rect.left += self.area.left
        self.boundrect.top += self.area.top
        self.boundrect.left += self.area.left

    def enter(self, leaving_area, sprite):
        # The sprite has to be moving in the same
        # direction as the offset
        down, right = self.offset
        if down == sprite.vmove and down or right == sprite.hmove and right:
            leaving_area.remove(sprite)
            self.to.add(sprite)
            sprite.boundtop = sprite.boundrect.top + down
            sprite.rect.left = sprite.boundrect.left + right

    def update(self, t):
        r = super(Portal, self).update(t)
        return r

    @classmethod
    def _connect_vertical(cls, area1, area2):
        # area1 has to be on top
        assert area1.top != area2.top
        if area1.top > area2.top:
            return cls._connect_vertical(area2, area1)

        portal_left = max(area1.left, area2.left)
        portal_width = min(area1.left + area1.width, area2.left + area2.width)

        area1.create_sprite(Portal,
                            topleft=(area1.height - 2,
                                     portal_left - area1.left),
                            to=area2,
                            offset=(1, 0),
                            height=1, width=portal_width)
        area2.create_sprite(Portal,
                            topleft=(2, portal_left - area2.left),
                            to=area1,
                            offset=(-1, 0),
                            height=1, width=portal_width)

    @classmethod
    def _connect_horizontal(cls, area1, area2):
        # area1 has to be on left
        assert area1.left != area2.left
        if area1.left > area2.left:
            return cls._connect_horizontal(area2, area1)

        height = area2.height

        # When connecting horizontal areas, the right area needs
        # to overlap this area to make room for the sprite. The
        # overlap will be invisible.
        area2.left -= 50
        area2.width += 50
        for sprite in area2:
            sprite.rect.left += 50

        portal_top = max(area1.top, area2.top)
        portal_height = min(area1.top + area1.height, area2.top + area2.height) - portal_top

        area1.create_sprite(Portal,
                            topleft=(portal_top - area1.top,
                                     area2.left - area1.left + 49),
                            to=area2,
                            offset=(0, 1),
                            height=portal_height, width=1)
        area2.create_sprite(Portal,
                            topleft=(portal_top - area2.top, 0),
                            to=area1,
                            offset=(0, -1),
                            height=portal_height, width=1)

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
        if isinstance(sprite, Portal):
            self.portals.add(sprite)
        self.bound_group.add(sprite)

    def remove(self, sprite):
        self.bound_group.remove(sprite)

    def _sprite_key(self, sprite):
        pushedby_count = 0
        if getattr(sprite, 'pushedby', None) is None:
            return 0
        else:
            return self._sprite_key(sprite.pushedby) - 1

    def update(self, ticks):
        self.bound_group._spritelist.sort(key=self._sprite_key)
        self.bound_group.update(ticks)
        for bound_sprite in self.bound_group:
            if isinstance(bound_sprite, Portal):
                continue

            try:
                self.check_collision(bound_sprite)
            except CancelEvent:
                pass

        def sprite_key(sprite):
            try:
                return sprite.boundtop
            except:
                return sprite.rect.top

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

        bound_sprite.boundrect = pygame.Rect(
            min(max(self.left, rect.left),
                self.left + self.width - rect.width),
            min(max(self.top, rect.top),
                self.top + self.height - rect.height),
            rect.width,
            rect.height)

        bound_sprite.rect.top = rect.top - bound_sprite.rect.height + bound_sprite.height
        bound_sprite.rect.left = rect.left
        
        return topleft != (bound_sprite.boundtop, bound_sprite.boundleft)

    def check_collision(self, bound_sprite):
        self.keep_inside(bound_sprite)
        try:
            lastmovebound = bound_sprite.lastmovebound
        except AttributeError:
            return "not applicable"

        try:
            if bound_sprite.__checking_collisions:
                return "already checked"
        except AttributeError:
            bound_sprite.__checking_collisions = 0
            print "new"

        try:
            bound_sprite.__checking_collisions += 1
            hit = []
            for entered_portal in pygame.sprite.spritecollide(
                lastmovebound,
                [Bound(s) for s in self.portals],
                False):

                if entered_portal.sprite is bound_sprite:
                    continue
                entered_portal.enter(self, bound_sprite)
                hit.append(entered_portal)
            return hit
        finally:
            bound_sprite.__checking_collisions -= 1

    def on_movement(self, event):
        self.check_collision(event.sprite)

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
