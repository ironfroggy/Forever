import pygame
from pygame.sprite import Sprite
from pygame import Surface, Rect

from foreverdrive.modes import Mode
from foreverdrive.mapgeneration import MapGenerator

ROOMS = 400

class MapDisplayMode(Mode):

    def __init__(self, game):
        super(MapDisplayMode, self).__init__(game)

        self.generator = MapGenerator()
        self.rooms_left = ROOMS

        room = self.generator.rooms[0]
        self.renderRoom(room)

    def renderRoom(self, room):
        c = 255.0*(float(self.rooms_left)/ROOMS)
        sprite = Sprite()
        sprite.image = Surface((room.rect.width, room.rect.height)).convert_alpha()
        sprite.rect = Rect(room.rect.left+250, room.rect.top+250, room.rect.width, room.rect.height)
        sprite.image.fill((c * room.template.c[0], c * room.template.c[1], c * room.template.c[2]))
        self.background.tile_group.add(sprite)

    def update(self, tick):
        if self.rooms_left >= 0:
            self.rooms_left -= 1
            self.generator, room = self.generator.addRandomRoom()

            self.renderRoom(room)
