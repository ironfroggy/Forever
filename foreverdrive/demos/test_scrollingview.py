from foreverdrive.demos.test_boundarea import *
from foreverdrive.modes.scrolling import ScrollingMode


class ScrollingModeTest(TestMode, ScrollingMode):
    area_size = (5, 5)

    def __init__(self, *args, **kwargs):
        ScrollingMode.__init__(self, *args, **kwargs)
        area = BoundArea("default_tile.png",
                         size=self.area_size,
                         topleft=(125, 175))
        self.areas.append(area)
        self.groups.append(area)


def main():
    game = ForeverMain(initmode=ScrollingModeTest)
    game.run()

if __name__ == '__main__':
    main()
