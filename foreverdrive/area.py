import pygame
from foreverdrive import get_media_path

class TileArea(object):
    def __init__(self, image_path, size):
        self.image = pygame.image.load(get_media_path(image_path)).convert()
        self.screen = pygame.display.get_surface()

        tg = self.tile_group = pygame.sprite.RenderUpdates()
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                sprite = pygame.sprite.Sprite()
                sprite.image = self.image
                sprite.rect = self.image.get_rect()
                sprite.rect.top = self.image.get_height() * y
                sprite.rect.left = self.image.get_width() * x
                tg.add(sprite)

    def update_and_draw(self, ticks):
        tg = self.tile_group
        screen = self.screen

        tg.update(ticks)
        return tg.draw(screen)
