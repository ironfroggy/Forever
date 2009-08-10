from random import randint, choice, uniform

from pygame import Rect
from pygame.sprite import collide_rect

MIN = 2
MAX = 4

def w_choice(lst):
    """Like random.choice() but expects items to be a 2-tuple
    of (item, weight).
    """
    n = uniform(0, 1)
    for item, weight in lst:
        if n < weight:
            break
        n = n - weight
    return item

class MapConflict(Exception):
    pass

class RoomTemplate(object):

    up_chance = 1
    down_chance = 1
    right_chance = 1
    left_chance = 1

    c = (1.0, 1.0, 1.0)

    def __init__(self, width_range=None, height_range=None):
        if width_range:
            self.width_range = width_range
        if height_range:
            self.height_range = height_range

        self._width_ranges = {}
        self._height_ranges = {}

        self.next = {'up':[], 'down': [], 'left': [], 'right': []}

    def getTemplateAndDirection(self, exclude=()):
        direction = None
        while direction in exclude or not direction:
            direction = self.getRandomDirection()

        if self.next[direction]:
            template = w_choice(self.next[direction])
        else:
            return self.getTemplateAndDirection(exclude + (direction,))
        
        return template, direction

    def makeRandomNeighbor(self, from_room, direction):
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
        height = randint(*self.height_range)
        width = randint(*self.width_range)

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

    def _getSideRange(self, base, room_length, new_length, minimum):
        #return (base - new_length + minimum), (base + room_length - new_length - minimum)
        upper = base + new_length - minimum
        return base, upper

    def getRandomPositionAt(self, from_room, (width, height), direction):
        rect = from_room.rect

        if direction == 'up':
            top = rect.top - height
            left = randint(*self._getSideRange(rect.left, rect.width, width, MIN))

        elif direction == 'left':
            left = rect.left - width
            top = randint(*self._getSideRange(rect.top, rect.height, height, MIN))

        elif direction == 'down':
            top = rect.top + rect.height
            left = randint(*self._getSideRange(rect.left, rect.width, width, MIN))

        elif direction == 'right':
            left = rect.left + rect.width
            top = randint(*self._getSideRange(rect.top, rect.height, height, MIN))

        return left, top

    def getRandomRoom(self, all_rooms):
        rooms = [r for r in all_rooms if r.wants_neighbors]
        i = randint(0, len(rooms) - 1)
        return rooms[i]


class MainRoomTemplate(RoomTemplate):

    def _getSideRange(self, base, room_length, new_length, minimum):
        lower = base - new_length/2 + room_length/2
        return (lower, lower)


class ConnectingRoomTemplate(RoomTemplate):

    def getRandomRoom(self, all_rooms):
        rooms = [r for r in all_rooms if isinstance(r.template, ConnectingRoomTemplate) and r.wants_neighbors]
        if rooms:
            i = randint(0, len(rooms) - 1)
            return rooms[i]
        else:
            return super(ConnectingRoomTemplate, self).getRandomRoom(all_rooms)

    def _getSideRange(self, base, room_length, new_length, minimum):
        lower = base + room_length/2 - new_length/2
        return (lower, lower)
        


template = RoomTemplate()

class Room(object):
    def __init__(self, *args, **kwargs):
        self.template = kwargs.pop('template', RoomTemplate())
        self.rect = Rect(*args, **kwargs)
        self.wants_neighbors = 10
        self.neighbors = set()

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

    def __init__(self, rooms=None, last_room=None):
        if rooms is None:
            self.rooms = (Room(0, 0, randint(MIN, MAX), randint(MIN, MAX)),)
        else:
            self.rooms = rooms

        if last_room is None:
            self.last_room = self.rooms[0]
        else:
            self.last_room = last_room

    def __iter__(self):
        return iter(self.rooms)

    def proposeNewRoom(self, from_room, new_room):
        """Finds if the new room fits into the map. It cannot overlap existing rooms.

        This is done by inflating the new_room by 1 pixel on all sides and allowing
        it to overlap the room its actually connected to.
        """

        new_room = new_room.rect
        new_room = Room(new_room.left - 1, new_room.top - 1, new_room.width + 2, new_room.height + 2)

        for room in self.rooms:
            if room is from_room:
                continue
            if collide_rect(new_room, room):
                from_room.wants_neighbors -= 1
                return False
        return True

    def addRoom(self, from_room, new_room):
        if self.proposeNewRoom(from_room, new_room):
            from_room.neighbors.add(new_room)
            return MapGenerator(rooms=self.rooms + (new_room,), last_room=new_room)
        else:
            raise MapConflict("Room collides with existing room(s)")

    def addRandomRoom(self):
        while True:
            try:
                return self._addRandomRoom()
            except (MapConflict, TypeError), e:
                continue

    def _addRandomRoom(self):
        last_template = self.last_room.template
        from_room = last_template.getRandomRoom(self.rooms)

        template, direction = from_room.template.getTemplateAndDirection()

        room = template.makeRandomNeighbor(from_room, direction)
        return self.addRoom(from_room, room), room

