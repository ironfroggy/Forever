from foreverdrive.base import ForeverMain
from foreverdrive.modes.map import MapDisplayMode
from foreverdrive.area import AreaManager

def report(event):
    print event.sprite.name, "entered", event.entered.name            

objects = []


def main():
    game = ForeverMain(initmode=MapDisplayMode)
    game.run()

if __name__ == '__main__':
    main()
