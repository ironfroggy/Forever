from foreverdrive.base import ForeverMain
from foreverdrive.modes.map import MapDisplayMode
from foreverdrive.area import AreaManager

from foreverdrive.mapgeneration import MapGenerator, Room, RoomTemplate


hallway_template_h = RoomTemplate(width_range=(5, 10), height_range=(10, 50))
hallway_template_h.c = (1.0, 0.6, 0.6)
hallway_template_w = RoomTemplate(width_range=(10, 50), height_range=(5, 10))
hallway_template_w.c = (0.6, 1.0, 0.6)

main_room_template = RoomTemplate(width_range=(20, 30), height_range=(20, 30))
main_room_template.c = (0.6, 0.6, 1.0)

for d in ('up', 'down', 'left', 'right'):
    main_room_template.next[d].extend([hallway_template_w, hallway_template_h])

hallway_template_h.next['up'].extend((main_room_template,))
hallway_template_h.next['down'].extend((main_room_template,))
hallway_template_w.next['left'].extend((main_room_template,))
hallway_template_w.next['right'].extend((main_room_template,))

class MapDisplayModeTest(MapDisplayMode):

    def __init__(self, game):
        super(MapDisplayModeTest, self).__init__(game)

        room = Room(0, 0, 50, 50)
        room.template = main_room_template
        self.generator = MapGenerator(rooms=(room,))
    

def main():
    game = ForeverMain(initmode=MapDisplayModeTest)
    game.run()

if __name__ == '__main__':
    main()
