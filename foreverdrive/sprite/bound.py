"""For any sprites that have to interact with each other in some
simulated way, the foreverdrive.sprite.bound module will provide
the facilities to do that. This includes collision detection and
correction, applying force, and constraints.
"""

from pygame.sprite import Sprite
from pygame import Rect

class Bound(object):
    """A Bound object interacts with others with simulated physics.

    This appears as a 'sprite' to pygame routines by having 'rect'
    and/or 'radius'.
    """

    def __init__(self, area, rect, sprite):
        """Initializes the bound object.

        @param area: The area is a group of bounds to interact with.
        @param rect: The position and size of the bound
        @param sprite: A pygame sprite-like object that is moved
                       with the bound and renders its representation.
        """

        self.area = area
        self.rect = rect
        self.sprite = sprite

        # Velocity is in "pixels per second"
        self.veloc_x = 0.0
        self.veloc_y = 0.0

        self.lastupdate = 0

    def update(self, tick):
        passed = tick - self.lastupdate
        self.rect.top += self.veloc_y / 1000.0
        self.rect.left += self.veloc_x / 1000.0


class BoundSprite(Sprite):
    """A bound sprite is in one group, a BoundGroup, which defines its
    boundries. The BoundSprite can move, but cannot go past the boundries
    or overlap other BoundSprite in the group.
    """

    slowdown = 1.0

    def __init__(self, *args, **kwargs):
        super(BoundSprite, self).__init__(*args, **kwargs)

        self.velocity = (0.0, 0.0)
        self.forces = []

    @property
    def rect(self):
        try:
            rect = Rect(self._rect)
            rect.top /= 10
            rect.left /= 10
            rect.width /= 10
            rect.height /= 10
            return rect
        except AttributeError:
            rect = self.image.get_rect()
            rect.top *= 10
            rect.left *= 10
            rect.width *= 10
            rect.height *= 10
            self._rect = rect
            return self._rect

    def update(self, ticks):
        m = ticks / 1000.0

        if self.forces:
            right_forces, down_forces = zip(*self.forces)
            right_force_avg = sum(right_forces) / len(right_forces)
            down_force_avg = sum(down_forces) / len(down_forces)

            try:
                self.velocity = (right + (right_force_avg/m), down + (down_force_avg/m))
            except ZeroDivisionError:
                pass

        right, down = self.velocity
        slowdown = self.slowdown
        self.velocity = (right - right * (m / slowdown), down - down * (m / slowdown))

        right, down = self.velocity
        try:
            self._rect.move_ip(right*m*10, down*m*10)
        except AttributeError:
            self.rect
            self._rect.move_ip(right*m*10, down*m*10)

