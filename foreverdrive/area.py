from itertools import chain

import pygame
from foreverdrive import get_media_path

class TileArea(object):
    def __init__(self, image_path, size):
        self.image = pygame.image.load(get_media_path(image_path)).convert()
        self.screen = pygame.display.get_surface()

        self._top = 0
        self._left = 0

        tg = self.tile_group = pygame.sprite.RenderUpdates()
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                sprite = pygame.sprite.Sprite()
                sprite.image = self.image
                sprite.rect = self.image.get_rect()
                sprite.rect.top = self.image.get_height() * y
                sprite.rect.left = self.image.get_width() * x
                tg.add(sprite)

    def __iter__(self):
        return iter(self.tile_group)

    # When top/left change, all sprites change
    @property
    def top(self):
        return self._top
    @top.setter
    def top(self, new_top):
        change = new_top - self._top
        for sprite in self:
            sprite.rect.top += change

    @property
    def left(self):
        return self._left
    @left.setter
    def left(self, new_left):
        change = new_left - self._left
        for sprite in self:
            sprite.rect.left += change

    def update_and_draw(self, ticks):
        tg = self.tile_group
        screen = self.screen

        tg.update(ticks)
        return tg.draw(screen)

class BoundArea(TileArea):

    def __init__(self, *args, **kwargs):
        super(BoundArea, self).__init__(*args, **kwargs)
        self.bound_group = pygame.sprite.RenderUpdates()

    def __iter__(self):
        return chain(self.tile_group, self.bound_group)

    def add(self, sprite):
        self.bound_group.add(sprite)

    def update_and_draw(self, ticks):
        super(BoundArea, self).update_and_draw(ticks)
        self.bound_group.update(ticks)
        for bound_sprite in self.bound_group:
            if bound_sprite.top < self.top:
                bound_sprite.top = self.top
