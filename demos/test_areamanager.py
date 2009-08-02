from foreverdrive.base import ForeverMain
from foreverdrive.modes import Mode
from foreverdrive.area import AreaManager

class AreaManagingMode(Mode):

    def __init__(self, *args, **kwargs):
        super(AreaManagingMode, self).__init__(*args, **kwargs)
        self.areas = AreaManager(self)

    def first_entering(self):
#        area = self.areas.new_area((25, 25), (3, 6))
#        self.areas.new_area((0, 0), (9, 3), relative_to=area.bottom_left)
#        topright = self.areas.new_area((0, 0), (6, 3), relative_to=area.top_right)
#        self.areas.new_area((0, -150), (3, 3), relative_to=topright.bottom_right)        
        self.areas.new_areas([
            ((25, 25), (3, 6), None,
             [((0, 0), (4, 4), "bottom_left",
               [((0, 0), (5, 1), "top_right", None)]
               ),
              ((0, 0), (2, 2), "top_right", None),
              ]

             )])

def main():
    game = ForeverMain(initmode=AreaManagingMode)
    game.run()

if __name__ == '__main__':
    main()
