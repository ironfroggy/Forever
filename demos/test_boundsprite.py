import pygame
from pygame.locals import *
from pygame import Surface, Color
from pygame.sprite import Sprite

from foreverdrive.base import ForeverMain
from foreverdrive.area import TileArea
from foreverdrive.sprite.bound import BoundSprite, BoundGroup, WallSprite

def main():
    game = ForeverMain()

    group = BoundGroup()
    background = BoundSprite()
    background.image = Surface((500, 500))
    group.add(background)
    group.background = background

    def player():
        player = BoundSprite()
        player.image = Surface((25, 25))
        player.image.fill(Color(200, 50, 50))
        player.register_listeners(game.mode)
        player.rect
        player._rect.move_ip(300, 300)
        group.add(player)

    def make_box((x, y, w, h), cls=BoundSprite, color=Color(50, 200, 200), v=None):
        box = cls()
        box.image = Surface((w, h))
        box.image.fill(color)
        box.rect
        box._rect.move_ip(x*10, y*10)
        group.add(box)

        if v:
            box.velocity = v
        return box

    for x in xrange(4):
        for y in xrange(4):
            if x + y < 4:
                box = make_box((200 + x*50, 200 + y*50, 50, 50))
#    print "box2", id(make_box((300, 250, 50, 50), color=Color(200, 50, 200)))

    make_box((0, 0, 500, 20), cls=WallSprite, color=Color(100, 100, 100))
    make_box((0, 480, 500, 20), cls=WallSprite, color=Color(100, 100, 100))
    make_box((0, 20, 20, 460), cls=WallSprite, color=Color(100, 100, 100))
    make_box((480, 20, 20, 460), cls=WallSprite, color=Color(100, 100, 100))
    player()

    game.groups.append(group)


    print "player", id(player)
    game.run()

if __name__ == "__main__":
    main()
