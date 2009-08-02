from foreverdrive.demos.test_boundarea import *
from foreverdrive.base import ScrollingMode


class ScrollingModeTest(TestMode, ScrollingMode):
    area_size = (10, 10)

def main():
    game = ForeverMain(initmode=ScrollingModeTest)
    game.run()

if __name__ == '__main__':
    main()
