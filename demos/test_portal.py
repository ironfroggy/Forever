from foreverdrive.base import ForeverMain
from foreverdrive.modes.scrolling import ScrollingMode
from foreverdrive.area import BoundArea
from foreverdrive.sprite import Player, SolidSprite
from foreverdrive.sprite.portal import Portal

class PortalTest(ScrollingMode):

    def __init__(self, *args, **kwargs):
        super(PortalTest, self).__init__(*args, **kwargs)
        area = self.area = BoundArea("default_tile.png",
                              size=(5, 5),
                              topleft=(125, 125),
                              mode=self)
        self.groups.append(self.area)
        self.areas.append(area)

        # Area above
        print "above"
        area = BoundArea("default_tile.png",
                         size=(4, 4),
                         topleft=(-200, 100),
                         relative_to=self.areas[0].top_left,
                         mode=self)
        self.areas.append(area)
        self.groups.append(area)

        Portal._connect_vertical(self.areas[0], area)

        # Area left
        area = BoundArea("default_tile.png",
                         size=(2, 2),
                         topleft=(0, -100),
                         relative_to=self.areas[0].top_left,
                         mode=self)
        self.areas.append(area)
        self.groups.append(area)

        Portal._connect_horizontal(self.areas[0], area)

        # Area below
        area = BoundArea("default_tile.png",
                         size=(3, 10),
                         topleft=(0, 100),
                         relative_to=area, reltype="bottom_left",
                         mode=self)
        self.areas.append(area)
        self.groups.append(area)

        Portal._connect_vertical(self.areas[0], area)

        # Area right
        area = BoundArea("default_tile.png",
                         size=(10, 3),
                         topleft=(100, 0),
                         relative_to=self.areas[0].top_right,
                         mode=self)
        self.areas.append(area)
        self.groups.append(area)

        Portal._connect_horizontal(self.areas[0], area)

    def first_entering(self):
        self.new = False
        self.game.groups.append(self.area)

        sprite = Player(topleft=(self.area.top+50, self.area.left+50), imagename="default_player", area=self.area, height=25)
        sprite.register_listeners(self.game.mode)
        self.player = sprite
    
        self.areas[0].add(sprite)
        super(PortalTest, self).first_entering()

        self.make_cylinder(100, 100)

    def make_cylinder(self, x, y):
        obj = self.area.create_sprite(
            SolidSprite,
            topleft=(x, y),
            height=30,
            image_path="default_oildrum",
            name="block")

def main():
    game = ForeverMain(initmode=PortalTest)
    game.run()

if __name__ == '__main__':
    main()
