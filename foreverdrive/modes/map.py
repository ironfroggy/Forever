import pygame
from pygame.sprite import Sprite
from pygame import Surface, Rect

from foreverdrive.modes import Mode
from foreverdrive.mapgeneration import MapGenerator

ROOMS = 10000

class MapDisplayMode(Mode):

    def __init__(self, game):
        super(MapDisplayMode, self).__init__(game)

        self.generator = MapGenerator()
        self.rooms_left = ROOMS

    def update(self, tick):
        i = self.rooms_left
        if i >= 0:
            self.rooms_left -= 1
            self.generator, room = self.generator.addRandomRoom()

            c = 255.0*(float(i)/ROOMS)
            sprite = Sprite()
            sprite.image = Surface((room.rect.width, room.rect.height)).convert_alpha()
            sprite.rect = Rect(room.rect.left+250, room.rect.top+250, room.rect.width, room.rect.height)
            sprite.image.fill((c, c, c))
            self.background.tile_group.add(sprite)
        
