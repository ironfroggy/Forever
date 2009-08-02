from foreverdrive.demos.test_scrollingview import *
from foreverdrive.area import Portal

class MultiAreaTest(ScrollingModeTest):
    area_size = (5, 5)
    def __init__(self, *args, **kwargs):
        super(MultiAreaTest, self).__init__(*args, **kwargs)
        area = self.areas[0]

        area = BoundArea("default_tile.png",
                         size=(3, 10),
                         topleft=(0, 100),
                         relative_to=area.bottom_left)
        self.areas.append(area)
        self.groups.append(area)

        Portal._connect_vertical(*self.areas)

        area = BoundArea("default_tile.png",
                         size=(10, 3),
                         topleft=(100, -50),
                         relative_to=self.areas[0].top_right)
        self.areas.append(area)
        self.groups.append(area)

        Portal._connect_horizontal(self.areas[0], self.areas[2])

def main():
    game = ForeverMain(initmode=MultiAreaTest)
    game.run()

if __name__ == '__main__':
    main()
