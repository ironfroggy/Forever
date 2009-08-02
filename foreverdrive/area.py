from itertools import chain

import pygame
from foreverdrive import get_media_path

class TileArea(object):
    def __init__(self, image_path, size):
        self.image = pygame.image.load(get_media_path(image_path)).convert()
        self.screen = pygame.display.get_surface()

        self._top = 0
        self._left = 0
        self.width = self.image.get_width() * size[0]
        self.height = self.image.get_height() * size[1]

        tg = self.tile_group = pygame.sprite.RenderUpdates()
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                sprite = pygame.sprite.Sprite()
                sprite.image = self.image
                sprite.rect = self.image.get_rect()
                sprite.rect.top = self.image.get_height() * y
                sprite.rect.left = self.image.get_width() * x
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

class BoundArea(TileArea):

    def __init__(self, *args, **kwargs):
        super(BoundArea, self).__init__(*args, **kwargs)
        self.bound_group = pygame.sprite.RenderUpdates()

    def __iter__(self):
        return chain(self.tile_group, self.bound_group)

    def add(self, sprite):
        self.bound_group.add(sprite)

    def update(self, ticks):
        self.bound_group.update(ticks)
        for bound_sprite in self.bound_group:

            rect = bound_sprite.rect
            bound_sprite.rect = pygame.Rect(
                min(max(self.left, rect.left), self.left + self.width - rect.width),
                min(max(self.top, rect.top), self.top + self.width - rect.width),
                rect.width,
                rect.height)

    def draw(self, surface):
        return chain(
            super(BoundArea, self).draw(surface) +
            self.bound_group.draw(surface))


