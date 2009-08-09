from foreverdrive.base import ForeverMain
from foreverdrive.modes.map import MapDisplayMode
from foreverdrive.area import AreaManager

from foreverdrive.mapgeneration import MapGenerator, Room, RoomTemplate

HALL_WIDE = (3, 4)
HALL_LONG = (10, 20)

hallway_template_h = RoomTemplate(width_range=HALL_WIDE, height_range=HALL_LONG)
hallway_template_h.c = (1.0, 0.6, 0.6)
hallway_template_w = RoomTemplate(width_range=HALL_LONG, height_range=HALL_WIDE)
hallway_template_w.c = (0.6, 1.0, 0.6)

MAIN_SIZE = (10, 15)

main_room_template = RoomTemplate(width_range=MAIN_SIZE, height_range=MAIN_SIZE)
main_room_template.c = (0.6, 0.6, 1.0)

HALL_EXTEND_CHANCE = 0.1
HALL_TO_MAIN_CHANCE = 0.9

hallway_template_h.next['up'].extend([
        (hallway_template_w, HALL_EXTEND_CHANCE),
        (hallway_template_h, HALL_EXTEND_CHANCE * 2),
        (main_room_template, HALL_TO_MAIN_CHANCE)
        ])
hallway_template_h.next['down'].extend([
        (hallway_template_w, HALL_EXTEND_CHANCE),
        (hallway_template_h, HALL_EXTEND_CHANCE * 2),
        (main_room_template, HALL_TO_MAIN_CHANCE)
        ])
hallway_template_w.next['left'].extend([
        (hallway_template_h, HALL_EXTEND_CHANCE),
        (hallway_template_w, HALL_EXTEND_CHANCE * 2),
        (main_room_template, HALL_TO_MAIN_CHANCE)
        ])
hallway_template_w.next['right'].extend([
        (hallway_template_h, HALL_EXTEND_CHANCE),
        (hallway_template_w, HALL_EXTEND_CHANCE * 2),
        (main_room_template, HALL_TO_MAIN_CHANCE)
])

small_hall = RoomTemplate(width_range=(1, 2), height_range=(1, 2))
small_hall.c = (1.0, 1.0, 0.6)
small_hall.next['up'] = [(main_room_template, 1.0)]
small_hall.next['down'] = [(main_room_template, 1.0)]

for d in ('up', 'down', 'left', 'right'):
    main_room_template.next[d].extend([(hallway_template_w, 0.1), (hallway_template_h, 0.1), (small_hall, 0.7)])

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
