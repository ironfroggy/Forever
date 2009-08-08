from random import randint

from pygame import Rect
from pygame.sprite import collide_rect

MIN = 1
MAX = 10

class MapConflict(Exception):
    pass

class Room(object):
    def __init__(self, *args, **kwargs):
        self.rect = Rect(*args, **kwargs)

class MapGenerator(object):
    """Randomly generates maps.

    Starts with one room and proceeds with a series of random
    modifications from a set of operations:
    - Expand to top, left, right, or bottom
    - Shrink from top, left, right, or bottom
    - Add area to top, left, right, or bottom

    At each operation, the proposed new set of areas is checked
    for collisions and is not used if there are any.
    """

    def __init__(self, rooms=None):
        if rooms is None:
            self.rooms = (Room(0, 0, randint(0, 20), randint(0, 20)),)
        else:
            self.rooms = rooms

    def __iter__(self):
        return iter(self.rooms)

    def getRandomRoom(self):
        i = randint(0, len(self.rooms) - 1)
        return self.rooms[i]

    def proposeNewRoom(self, new_room):
        for room in self.rooms:
            if collide_rect(new_room, room):
                return False
        return True

    def addRoom(self, new_room):
        if self.proposeNewRoom(new_room):
            return MapGenerator(rooms=self.rooms + (new_room,))
        else:
            raise MapConflict("Room collides with existing room(s)")

    def addRandomRoom(self):
        try:
            return self._addRandomRoom()
        except (MapConflict, ValueError), e:
            return self.addRandomRoom()

    def _addRandomRoom(self):
        from_room = self.getRandomRoom().rect
        direction = ('left', 'up', 'right', 'down')[randint(0, 3)]

        height = randint(MIN, MAX)
        width = randint(MIN, MAX)

        if direction == 'up':
            top = from_room.top - height
            left = randint(from_room.left - width + MIN, from_room.left + from_room.width - width - MIN)

        elif direction == 'left':
            left = from_room.left - width
            top = randint(from_room.top - height + MIN, from_room.top + from_room.height - height - MIN)

        elif direction == 'down':
            top = from_room.top + from_room.height
            left = randint(from_room.left - width + MIN, from_room.left + from_room.width - MIN)

        elif direction == 'right':
            left = from_room.left + from_room.width
            top = randint(from_room.top - height + 2, from_room.top + from_room.height - MIN)


        room = Room(left, top, width, height)
        return self.addRoom(room), room

