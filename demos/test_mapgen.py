from foreverdrive.base import ForeverMain
from foreverdrive.modes.map import MapDisplayMode
from foreverdrive.area import AreaManager

from foreverdrive.mapgeneration import MapGenerator, Room, RoomTemplate


hallway_template_h = RoomTemplate(width_range=(1, 2), height_range=(2, 5))
hallway_template_h.c = (1.0, 0.6, 0.6)
hallway_template_w = RoomTemplate(width_range=(2, 10), height_range=(1, 2))
hallway_template_w.c = (0.6, 1.0, 0.6)

main_room_template = RoomTemplate(width_range=(4, 6), height_range=(4, 6))
main_room_template.c = (0.6, 0.6, 1.0)

for d in ('up', 'down', 'left', 'right'):
    main_room_template.next[d].extend([(hallway_template_w, 0.5), (hallway_template_h, 0.5)])

HALL_EXTEND_CHANCE = 0.8
HALL_TO_MAIN_CHANCE = 0.2

hallway_template_h.next['up'].extend([(hallway_template_w, HALL_EXTEND_CHANCE), (main_room_template, HALL_TO_MAIN_CHANCE)])
hallway_template_h.next['down'].extend([(hallway_template_w, HALL_EXTEND_CHANCE), (main_room_template, HALL_TO_MAIN_CHANCE)])
hallway_template_w.next['left'].extend([(hallway_template_h, HALL_EXTEND_CHANCE), (main_room_template, HALL_TO_MAIN_CHANCE)])
hallway_template_w.next['right'].extend([(hallway_template_h, HALL_EXTEND_CHANCE), (main_room_template, HALL_TO_MAIN_CHANCE)])

class MapDisplayModeTest(MapDisplayMode):

    def __init__(self, game):
        super(MapDisplayModeTest, self).__init__(game)

        room = self.generator.rooms[0]
        room.template = main_room_template

def main():
    game = ForeverMain(initmode=MapDisplayModeTest)
    game.run()

if __name__ == '__main__':
    main()
