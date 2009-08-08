from random import randint, choice

from pygame import Rect
from pygame.sprite import collide_rect

MIN = 10
MAX = 30

class MapConflict(Exception):
    pass

class RoomTemplate(object):

    up_chance = 1
    down_chance = 1
    right_chance = 1
    left_chance = 1
    next = ()

    c = (1.0, 1.0, 1.0)

    def __init__(self, width_range=None, height_range=None):
        if not width_range:
            width_range = (MIN, MAX)
        if not height_range:
            height_range = (MIN, MAX)
        self.width_range = width_range
        self.height_range = height_range
        self._width_ranges = {}
        self._height_ranges = {}

        self.next = {'up':[], 'down': [], 'left': [], 'right': []}

    def getTemplateAndDirection(self, exclude=()):
        direction = None
        while direction in exclude or not direction:
            direction = self.getRandomDirection()

        if self.next[direction]:
            template = choice(self.next[direction])
        else:
            return self.getTemplateAndDirection(exclude + (direction,))
        
        return template, direction

    def getRandomRoom(self, from_room, direction):
        width, height = self.getRandomSize(from_room, direction)

        left, top = self.getRandomPositionAt(from_room, (width, height), direction)

        return Room(left, top, width, height, template=self)

    def getRandomDirection(self, from_room=None):
        template = from_room.template if from_room is not None else self
        direction_sampling = (('left',) * template.left_chance +
                              ('up',) * template.up_chance +
                              ('right',) * template.right_chance +
                              ('down',) * template.down_chance)
        return choice(direction_sampling)

    def getRandomSize(self, from_room, direction):
        height = randint(*from_room.template.getNeighborHeightRange(direction))
        width = randint(*from_room.template.getNeighborWidthRange(direction))

        return width, height

    def getNeighborHeightRange(self, direction):
        try:
            return choice(self._height_ranges[direction])
        except KeyError:
            return self.height_range

    def getNeighborWidthRange(self, direction):
        try:
            return choice(self._width_ranges[direction])
        except KeyError:
            return self.width_range

    def getRandomPositionAt(self, from_room, (width, height), direction):
        rect = from_room.rect

        if direction == 'up':
            top = rect.top - height
            left = randint(rect.left - width + MIN, rect.left + rect.width - width - MIN)

        elif direction == 'left':
            left = rect.left - width
            top = randint(rect.top - height + MIN, rect.top + rect.height - height - MIN)

        elif direction == 'down':
            top = rect.top + rect.height
            left = randint(rect.left - width + MIN, rect.left + rect.width - MIN)

        elif direction == 'right':
            left = rect.left + rect.width
            top = randint(rect.top - height + MIN, rect.top + rect.height - MIN)

        return left, top


template = RoomTemplate()

class Room(object):
    def __init__(self, *args, **kwargs):
        self.template = kwargs.pop('template', RoomTemplate())
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
            self.rooms = (Room(0, 0, randint(MIN, MAX), randint(MIN, MAX)),)
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
        while True:
            try:
                return self._addRandomRoom()
            except (MapConflict, ValueError), e:
                continue

    def _addRandomRoom(self):
        from_room = self.getRandomRoom()

        template, direction = from_room.template.getTemplateAndDirection()

        room = template.getRandomRoom(from_room, direction)
        return self.addRoom(room), room

