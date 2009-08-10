from foreverdrive.base import ForeverMain
from foreverdrive.modes.scrolling import ScrollingMode
from foreverdrive.area import BoundArea
from foreverdrive.sprite import Player
from foreverdrive.sprite.portal import Portal

class PortalTest(ScrollingMode):

    def __init__(self, *args, **kwargs):
        super(PortalTest, self).__init__(*args, **kwargs)
        area = self.area = BoundArea("default_tile.png",
                              size=(5, 5),
                              topleft=(125, 125))
        self.groups.append(self.area)
        self.areas.append(area)

        # Area below
        area = BoundArea("default_tile.png",
                         size=(3, 10),
                         topleft=(0, 100),
                         relative_to=area.bottom_left)
        self.areas.append(area)
        self.groups.append(area)

        Portal._connect_vertical(*self.areas)

        # Area right
        area = BoundArea("default_tile.png",
                         size=(10, 3),
                         topleft=(100, 0),
                         relative_to=self.areas[0].top_right)
        self.areas.append(area)
        self.groups.append(area)

        Portal._connect_horizontal(self.areas[0], self.areas[2])

        # Area above
        print "above"
        area = BoundArea("default_tile.png",
                         size=(4, 4),
                         topleft=(-200, 100),
                         relative_to=self.areas[0].top_left)
        self.areas.append(area)
        self.groups.append(area)

        Portal._connect_vertical(self.areas[0], self.areas[3])

        # Area left
        area = BoundArea("default_tile.png",
                         size=(2, 2),
                         topleft=(0, -100),
                         relative_to=self.areas[0].top_left)
        self.areas.append(area)
        self.groups.append(area)

        Portal._connect_horizontal(self.areas[0], self.areas[4])


    def first_entering(self):
        self.new = False
        self.game.groups.append(self.area)

        sprite = Player(topleft=(self.area.top+50, self.area.left+50), imagename="default_player", area=self.area, height=25)
        sprite.register_listeners(self.game.mode)
        self.player = sprite
    
        self.areas[0].add(sprite)
        super(PortalTest, self).first_entering()

def main():
    game = ForeverMain(initmode=PortalTest)
    game.run()

if __name__ == '__main__':
    main()
