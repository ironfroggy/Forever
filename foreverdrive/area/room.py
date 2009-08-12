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

        upleft = self.spriteset.load("roomwall", "concave_upleft")
        upleft_width = upleft.get_width()
        left = self.width - upleft_width
        top = self.height - upleft.get_height()
        self.create_sprite(ImmovableSprite, (top, left), slotgroup="roomwall", slotname="concave_upleft")

        self._decorate_wall('up', upright.get_width(), left)
        self._decorate_wall('down', upright.get_width(), left)
        self._decorate_wall('left', upleft.get_height(), top)
        self._decorate_wall('right', upleft.get_height(), top)

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
            
    def _decorate_right_wall(self, lower, upper):
        """The RIGHT wall faces LEFT."""

        flat_left = self.spriteset.load("roomwall", "flat_left")
        flat_left_height = flat_left.get_height()
        left = self.width - flat_left.get_width()
        distance = upper - lower
        top = lower
        while top + flat_left_height <= upper:
            print self.create_sprite(ImmovableSprite, (top, left), slotgroup="roomwall", slotname="flat_left").boundrect
            top += flat_left_height
        remaining = abs(upper - top)
        if remaining:
            last = self.create_sprite(ImmovableSprite, (top, left), slotgroup="roomwall", slotname="flat_left")
            image = Surface((last.image.get_width(), remaining), 0).convert_alpha()
            image.blit(last.image, image.get_clip())
            last.image = image

    def _get_length_by_facing(self, tile, facing):
        if facing in ('up', 'down'):
            return tile.get_width()
        else:
            return tile.get_height()

    def _get_wall_away(self, facing, tile):
        if facing == 'up':
            return self.width - tile.get_width()
        elif facing == 'left':
            return self.height - tile.get_height()
        return 0

    def _get_topleft(self, facing, lower, away):
        if facing in ('up', 'down'):
            return (away, lower)
        else:
            return (lower, away)

    def _decorate_wall(self, facing, lower, upper):
        """The RIGHT wall faces LEFT."""

        tile = self.spriteset.load("roomwall", "flat_" + facing)
        # The length in the direction of the wall being decorated
        tile_length = self._get_length_by_facing(tile, facing)
        away = self._get_wall_away(facing, tile)
        remaining = upper - lower
        while lower + tile_length <= upper:
            self.create_sprite(ImmovableSprite, self._get_topleft(facing, lower, away), slotgroup="roomwall", slotname="flat_" + facing)
            lower += tile_length
        remaining = abs(upper - lower)
        if remaining:
            last = self.create_sprite(ImmovableSprite, self._get_topleft(facing, lower, away), slotgroup="roomwall", slotname="flat_" + facing)
            image = Surface(self._get_topleft(facing, self._get_length_by_facing(last.image, facing), remaining), 0).convert_alpha()
            image.blit(last.image, image.get_clip())
            last.image = image
