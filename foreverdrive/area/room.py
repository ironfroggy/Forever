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

        lower = upright.get_width()        
        self._decorate_wall('up', lower, left)
        self._decorate_wall('down', lower, left)
        lower = upleft.get_height()

        right_lower = lower
        for (wall_length, portal_length) in self._get_portals_at_side('right'):
            self._decorate_wall('left', right_lower, wall_length)
            right_lower += wall_length + portal_length

        self._decorate_wall('right', lower, top)

    def _get_portals_at_side(self, side):
        """Returns a list of 2-tuples of int pairs, which denote
        length of wall and length of portal.
        """

        side_to_pos = {
            'up': 'left', 'left': 'top', 'right': 'top', 'down': 'left'
            }
        side_to_length = {
            'up': 'width', 'left': 'height', 'right': 'height', 'down': 'width'
            }

        results = []

        # Get the neighbors on this side and sort them in the order on the map
        neighbors = self.get_neighbors_at_side(side)
        neighbors.sort(key=lambda N: getattr(N, side_to_attr[side]))

        w_pos = getattr(self, side_to_pos[side])
        for neighbor in neighbors:
            # Where and how large is the neighbor?
            n_pos = getattr(neighbor, side_to_pos[side])
            n_length = getattr(neighbor, side_to_length[side])

            if n_pos <= w_pos:
                w_length = 0
            else:
                w_length = n_pos - w_pos

            results.append((w_length, n_length))

            w_pos = n_pos + n_length

        return results

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
