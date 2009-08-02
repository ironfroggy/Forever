from itertools import chain

import pygame
from foreverdrive import get_media_path
from foreverdrive.sprite import Sprite

class TileArea(object):
    def __init__(self, image_path, size, topleft=(0, 0), relative_to=None):
        self.image = pygame.image.load(get_media_path(image_path)).convert()
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

        tg = self.tile_group = pygame.sprite.RenderUpdates()
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
            sprite.rect.top += change
        self.update_rect()

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
        return (self.top, self.left + self.width)

    def update_and_draw(self, ticks):
        self.update(ticks)
        return self.draw(self.screen)

    def update(self, ticks):
        self.tile_group.update(ticks)

    def draw(self, screen):
        screen = self.screen
        return self.tile_group.draw(screen)

    def update(self, ticks):
        pass

    def create_sprite(self, cls, *args, **kwargs):
        print cls, Sprite
        sprite = cls(*args, **kwargs)
        print sprite.rect
        sprite.rect.top += self.top
        sprite.rect.left += self.left
        print sprite.rect
        self.add(sprite)
        return sprite

class Portal(Sprite):

    def __init__(self, *args, **kwargs):
        self.to = kwargs.pop('to', None)
        kwargs['image_path'] = "default_portal.png"
        super(Portal, self).__init__(*args, **kwargs)

    def enter(self, leaving_area, sprite):
        leaving_area.remove(sprite)
        self.to.add(sprite)

class BoundArea(TileArea):

    def __init__(self, *args, **kwargs):
        super(BoundArea, self).__init__(*args, **kwargs)
        self.bound_group = pygame.sprite.RenderUpdates()
        self.portals = pygame.sprite.RenderUpdates()

    def __iter__(self):
        return chain(self.tile_group, self.bound_group)

    def add(self, sprite):
        if isinstance(sprite, Portal):
            self.portals.add(sprite)
        self.bound_group.add(sprite)

    def remove(self, sprite):
        self.bound_group.remove(sprite)

    def update(self, ticks):
        self.bound_group.update(ticks)
        for bound_sprite in self.bound_group:
            if isinstance(bound_sprite, Portal):
                continue

            rect = bound_sprite.rect
            bound_sprite.rect = pygame.Rect(
                min(max(self.left, rect.left), self.left + self.width - rect.width),
                min(max(self.top, rect.top), self.top + self.height - rect.height),
                rect.width,
                rect.height)

            for entered_portal in pygame.sprite.spritecollide(bound_sprite, self.portals, False):
                entered_portal.enter(self, bound_sprite)

    def draw(self, surface):
        return chain(
            super(BoundArea, self).draw(surface) +
            self.bound_group.draw(surface))


