"""For any sprites that have to interact with each other in some
simulated way, the foreverdrive.sprite.bound module will provide
the facilities to do that. This includes collision detection and
correction, applying force, and constraints.
"""

import math

import pygame
from pygame.sprite import Sprite, RenderUpdates
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

    stuck = (0, 0, 0, 0)

    def __init__(self, *args, **kwargs):
        super(BoundSprite, self).__init__(*args, **kwargs)

        self.velocity = (0.0, 0.0)
        self.controlled_force = Force()
        self.forces = [self.controlled_force]

    @property
    def group(self):
        return self.groups()[0]

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

        self._move(m)

    def _move(self, m, v=None):
        if not v:
            right, down = self.velocity
        else:
            right, down = v

        self.rect
        su, sr, sd, sl = self.stuck
        if down > 0:
            if sd:
                down = 0
        elif down < 0:
            if su:
                down = 0
        if right > 0:
            if sr:
                right = 0
        elif right < 0:
            if sl:
                right = 0
        self._rect.move_ip(right*m*10, down*m*10)

        # Now that we've moved, check nearby to see if we're unblocked
        bu, br, bd, bl = self.group.blocked_sides(self)
        self.stuck = bu and su, br and sr, bd and sd, bl and sl

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


class WallSprite(BoundSprite):

    stuck = (1, 1, 1, 1) 
    slowdown = 0.1

    def update(self, ticks):
        pass


class BoundGroup(RenderUpdates):

    def __init__(self, *args, **kwargs):
        super(BoundGroup, self).__init__(*args, **kwargs)
        self.rect = Rect((0, 0, 5000, 5000))

    def sprites(self):
        sprite_list = super(BoundGroup, self).sprites()
        sprite_list.sort(key=lambda s: s is not self.background)
        return sprite_list

    def update(self, ticks):
        super(BoundGroup, self).update(ticks)

        m = ticks / 1000

        for sprite in self.sprites():
            if sprite is self.background:
                continue
            for hit_sprite in pygame.sprite.spritecollide(sprite, self, False):
                if hit_sprite is sprite or hit_sprite is self.background:
                    continue
                else:
                    a_x, a_y = sprite.velocity
                    a_d = math.sqrt(a_x*a_x + a_y*a_y)

                    b_x, b_y = hit_sprite.velocity
                    b_d = math.sqrt(b_x*b_x + b_y*b_y)

                    if a_d > b_d:
                        pushed = hit_sprite
                        pusher = sprite
                    else:
                        pushed = sprite
                        pusher = hit_sprite

                    x, y = pusher.velocity
                    cx, cy = pushed.velocity

                    su, sr, sd, sl = pusher.stuck
                    csu, csr, csd, csl = pushed.stuck
                    csx, csy = 1, 1

                    # sx, sy - 1 if current movement on that axis is allowed 
                    # Adjust to un-overlap
                    # In a given direction, if both are unstuck, adjust both
                    # In a given direction, if the one is stuck, adjust other

                    vx, vy = 0, 0
                    original_rect = Rect(pushed._rect)
                    B = -0.1

                    # pushing down
                    if y > 0:
                        if not csd:
                            pushed._rect.top += y
                            vy = y
                        else:
                            pusher._rect.top -= y/2
                            y *= B

                    # pushing up
                    elif y < 0:
                        if not csu:
                            pushed._rect.top += y
                            vy = y
                        else:
                            pusher._rect.top -= y/2
                            y *= B
                    
                    # pushing right
                    if x > 0:
                        if not csr:
                            pushed._rect.left += x
                            vx = x
                        else:
                            pusher._rect.left -= x/2
                            x *= B

                    # pushing left
                    elif x < 0:
                        if not csl:
                            pushed._rect.left += x
                            vx = x
                        else:
                            pusher._rect.left -= x/2
                            x *= B

                    # Pushed object is moved, but did it move inside something else?
                    # If so, retroactively make this a pushback.
                    if self.sprite_colliding(pushed):
                        pushed._rect = original_rect
                        pushed.velocity = ((cx + vx)/4, (cy + vy)/4)
                        pusher._rect.top -= y
                        pusher._rect.left -= x
                    else:
                        pushed.velocity = (cx + vx, cy + vy)
                        pusher.velocity = (x, y)


    def _stuck_for_direction(self, stuck_now, velocity):
        su, sr, sd, sl = stuck_now
        x, y = velocity

        if y < 0:
            su += 1
        elif y > 0:
            sd += 1
        if x > 0:
            sl += 1
        elif x < 0:
            sr += 1

        return su, sr, sd, sl

    def sprite_colliding(self, pushed):
        for sprite in pygame.sprite.spritecollide(pushed, self, False):
            if sprite is self.background or sprite is pushed:
                continue
            else:
                return True
        return False

    def blocked_sides(self, sprite):
        r = sprite._rect

        top = pygame.sprite.Sprite()
        top.rect = Rect(r.left, r.top - 1, r.width, 1)

        right = pygame.sprite.Sprite()
        right.rect = Rect(r.left + r.width + 1, r.top, 1, r.height)

        bottom = pygame.sprite.Sprite()
        bottom.rect = Rect(r.left, r.top + r.height + 1, r.width, 1)

        left = pygame.sprite.Sprite()
        left.rect = Rect(r.left - 1, r.top, 1, r.height)

        su, sr, sd, sl = 0, 0, 0, 0 
        if self.sprite_colliding(top):
            su = 1
        if self.sprite_colliding(right):
            sr = 1
        if self.sprite_colliding(bottom):
            sd = 1
        if self.sprite_colliding(left):
            sl = 1

        return su, sr, sd, sl
