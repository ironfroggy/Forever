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

    player = BoundSprite()
    player.image = Surface((50, 50))
    player.image.fill(Color(200, 50, 50))
    player.register_listeners(game.mode)
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

    print "box1", id(make_box((200, 200, 50, 50), v=(0, -150)))
    print "box2", id(make_box((300, 250, 50, 50), color=Color(200, 50, 200)))

    print "wall", id(make_box((0, 400, 500, 20), cls=WallSprite, color=Color(100, 100, 100)))

    game.groups.append(group)


    print "player", id(player)
    game.run()

if __name__ == "__main__":
    main()
