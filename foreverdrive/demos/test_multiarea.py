from foreverdrive.demos.test_scrollingview import *


class MultiAreaTest(ScrollingModeTest):
    def __init__(self, *args, **kwargs):
        super(MultiAreaTest, self).__init__(*args, **kwargs)
        area = self.areas[0]

        area = BoundArea("default_tile.png",
                         size=self.area_size,
                         topleft=(0, 100),
                         relative_to=area.bottom_left)
        self.areas.append(area)
        self.groups.append(area)


def main():
    game = ForeverMain(initmode=MultiAreaTest)
    game.run()

if __name__ == '__main__':
    main()
