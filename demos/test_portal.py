from foreverdrive.base import ForeverMain
from foreverdrive.modes.scrolling import ScrollingMode
from foreverdrive.area import BoundArea
from foreverdrive.sprite import Player, SolidSprite, default_spriteset
from foreverdrive.sprite.portal import Portal

class PortalTest(ScrollingMode):

    def __init__(self, *args, **kwargs):
        super(PortalTest, self).__init__(*args, **kwargs)
        main_area = self.area = BoundArea(default_spriteset,
                              size=(250, 250),
                              topleft=(150, 150),
                              mode=self)
        self.groups.append(main_area)
        self.areas.append(main_area)

        #  0123456789.123456
        #2-   ----
        #1-   |  |
        #0    |  |
        #1    |  |
        #2    ----
        #3 -------
        #4 --|   |----------
        #5   |   ||        |
        #6   |   |----------
        #7   -----
        #8    ---
        #9    | |
        #.    | |
        #1    | |
        #2    | |
        #3    | |
        #4    | |
        #5    | |
        #6    | |
        #7    ---


        # Area above
        print "above"
        area = BoundArea(default_spriteset,
                         size=(200, 200),
                         topleft=(-50, 200),
                         mode=self)
        self.areas.append(area)
        self.groups.append(area)

        Portal.connect(self.areas[0], area)

        # Area left
        area = BoundArea(default_spriteset,
                         size=(100, 100),
                         topleft=(150, 50),
                         mode=self)
        self.areas.append(area)
        self.groups.append(area)

        Portal.connect(self.areas[0], area)

        # Area below
        area = BoundArea(default_spriteset,
                         size=(150, 500),
                         topleft=(400, 150),
                         mode=self)
        self.areas.append(area)
        self.groups.append(area)

        Portal.connect(self.areas[0], area)

        # Area right
        area = BoundArea(default_spriteset,
                         size=(500, 150),
                         topleft=(200, 400),
                         mode=self)
        self.areas.append(area)
        self.groups.append(area)

        Portal.connect(self.areas[0], area)

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
