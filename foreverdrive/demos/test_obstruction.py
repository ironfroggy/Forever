from foreverdrive.base import ForeverMain
from foreverdrive.modes import Mode
from foreverdrive.area import AreaManager
from foreverdrive.sprite import Sprite

class AreaManagingMode(Mode):

    def __init__(self, *args, **kwargs):
        super(AreaManagingMode, self).__init__(*args, **kwargs)
        self.areas = AreaManager(self)

    def first_entering(self):
#        area = self.areas.new_area((25, 25), (3, 6))
#        self.areas.new_area((0, 0), (9, 3), relative_to=area.bottom_left)
#        topright = self.areas.new_area((0, 0), (6, 3), relative_to=area.top_right)
#        self.areas.new_area((0, -150), (3, 3), relative_to=topright.bottom_right)        
        area = self.areas.new_areas([
            ((125, 125), (6, 6), None, None)
            ])[0]

        sprite = area.create_sprite(Sprite,
                                    topleft=(100, 100),
                                    image_path="default_obstruction.png")


def main():
    game = ForeverMain(initmode=AreaManagingMode)
    game.run()

if __name__ == '__main__':
    main()
