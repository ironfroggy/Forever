"""For any sprites that have to interact with each other in some
simulated way, the foreverdrive.sprite.bound module will provide
the facilities to do that. This includes collision detection and
correction, applying force, and constraints.
"""

from pygame.sprite import Sprite
from pygame import Rect
from pygame.locals import *

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


class Force(object):

    def __iter__(self):
        return iter((self.x, self.y))

    x = 0
    y = 0


class BoundSprite(Sprite):
    """A bound sprite is in one group, a BoundGroup, which defines its
    boundries. The BoundSprite can move, but cannot go past the boundries
    or overlap other BoundSprite in the group.
    """

    slowdown = 0.25
    speed = 2

    def __init__(self, *args, **kwargs):
        super(BoundSprite, self).__init__(*args, **kwargs)

        self.velocity = (0.0, 0.0)
        self.controlled_force = Force()
        self.forces = [self.controlled_force]

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

        s = self.speed
        self.controlled_force.x = (s if self.keypressing_right else 0) + (-s if self.keypressing_left else 0)
        self.controlled_force.y = (s if self.keypressing_down else 0) + (-s if self.keypressing_up else 0)

        right, down = self.velocity
        if self.forces:
            right_forces, down_forces = zip(*self.forces)
            right_force_avg = sum(right_forces) / len(right_forces)
            down_force_avg = sum(down_forces) / len(down_forces)

            try:
                self.velocity = (right + (right_force_avg/m), down + (down_force_avg/m))
                right, down = self.velocity
            except ZeroDivisionError:
                pass

        slowdown = self.slowdown
        self.velocity = (right - right * (m / slowdown), down - down * (m / slowdown))

        right, down = self.velocity
        try:
            self._rect.move_ip(right*m*10, down*m*10)
        except AttributeError:
            self.rect
            self._rect.move_ip(right*m*10, down*m*10)

    def register_listeners(self, router):
        router.listen_arrows(self.handle_event)

    keypressing_up = False
    keypressing_down = False
    keypressing_left = False
    keypressing_right = False
    def handle_event(self, event):
        
        if event.type in (KEYDOWN, KEYUP):
            pressing = event.type == KEYDOWN
            if event.key == K_DOWN:
                self.keypressing_down = pressing
            elif event.key == K_UP:
                self.keypressing_up = pressing
            elif event.key == K_LEFT:
                self.keypressing_left = pressing
            elif event.key == K_RIGHT:
                self.keypressing_right = pressing
