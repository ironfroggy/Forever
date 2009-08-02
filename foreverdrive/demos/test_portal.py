from foreverdrive.demos.test_scrollingview import *
from foreverdrive.area import Portal

class MultiAreaTest(ScrollingModeTest):
    def __init__(self, *args, **kwargs):
        super(MultiAreaTest, self).__init__(*args, **kwargs)
        area = self.areas[0]

        area = BoundArea("default_tile.png",
                         size=self.area_size,
                         topleft=(-50, 100),
                         relative_to=area.bottom_left)
        self.areas.append(area)
        self.groups.append(area)

        self.areas[0].create_sprite(Portal, topleft=(249, 150), to=area, offset=(1, 0))
        self.areas[1].create_sprite(Portal, topleft=(-49, 50), to=self.areas[0], offset=(-1, 0))

def main():
    game = ForeverMain(initmode=MultiAreaTest)
    game.run()

if __name__ == '__main__':
    main()
