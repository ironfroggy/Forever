from foreverdrive.base import ForeverMain
from foreverdrive.modes import Mode
from foreverdrive.area import AreaManager

class AreaManagingMode(Mode):

    def __init__(self, *args, **kwargs):
        super(AreaManagingMode, self).__init__(*args, **kwargs)
        self.areas = AreaManager(self)

    def first_entering(self):
        area = self.areas.new_area((25, 25), (4, 8))
        self.areas.new_area((0, 0), (8, 4), relative_to=area.bottom_left)

def main():
    game = ForeverMain(initmode=AreaManagingMode)
    game.run()

if __name__ == '__main__':
    main()
