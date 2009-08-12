from pygame import Surface

from foreverdrive.sprite import ImmovableSprite
from foreverdrive.area import BoundArea


class Room(BoundArea):
    """Defines an area with walls, inside.

    Slotgroup: roomwall
    Slots: (The directions are named for the direction they *face*
    - flat_down
    - flat_up
    - flat_left
    - flat_right
    - concave_upright
    - concave_upleft
    - concave_downright
    - concave_downleft
    - convex_upright
    - convex_upleft
    - convex_downright
    - convex_downleft
    """

    def decorate(self):
        """Adds SolidSprite instances for walls, handling
        portals properly.

        There is a convex tile on each side of each portal.
        """

        self.create_sprite(ImmovableSprite, (0, 0), slotgroup="roomwall", slotname="concave_downright")

        left = self.width - self.spriteset.load("roomwall", "concave_downleft").get_width()
        self.create_sprite(ImmovableSprite, (0, left), slotgroup="roomwall", slotname="concave_downleft")

        upright = self.spriteset.load("roomwall", "concave_upright")
        top = self.height - upright.get_height()
        self.create_sprite(ImmovableSprite, (top, 0), slotgroup="roomwall", slotname="concave_upright")

        upleft_width = self.spriteset.load("roomwall", "concave_upleft").get_width()
        left = self.width - upleft_width
        self.create_sprite(ImmovableSprite, (top, left), slotgroup="roomwall", slotname="concave_upleft")

        self._decorate_bottom_wall(upright.get_width(), left)

    def _decorate_bottom_wall(self, lower, upper):
        flat_up = self.spriteset.load("roomwall", "flat_up")
        flat_up_width = flat_up.get_width()
        top = self.height - flat_up.get_height()
        distance = upper - lower
        left = lower
        while left + flat_up_width <= upper:
            self.create_sprite(ImmovableSprite, (top, left), slotgroup="roomwall", slotname="flat_up")
            left += flat_up_width
        remaining = upper - left
        if remaining:
            last = self.create_sprite(ImmovableSprite, (top, left), slotgroup="roomwall", slotname="flat_up")
            image = Surface((remaining, last.image.get_height()), 0).convert_alpha()
            image.blit(last.image, image.get_clip())
            last.image = image
            
