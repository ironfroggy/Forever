from foreverdrive.errors import PlacementError
from foreverdrive.sprite import Sprite, PerimeterSensoringMixin


class Portal(Sprite, PerimeterSensoringMixin):

    def __init__(self, *args, **kwargs):
        self.to = kwargs.pop('to', None)
        self.offset = kwargs.pop('offset', None)
        height = kwargs.pop('height', 100)
        width = kwargs.pop('width', 1)

        kwargs['image_path'] = "default_portal"
        super(Portal, self).__init__(*args, **kwargs)

        top, left = self.offset
        if left:
            self.rect.height = height
            self.rect.width = width

        self.boundrect.width = width
        self.boundrect.height = height

        self.show_bounds()

    def adjust_inside_area(self):
        self.rect.top += self.area.top
        self.rect.left += self.area.left
        self.boundrect.top += self.area.top
        self.boundrect.left += self.area.left

    def on_overlap(self, leaving_area, sprite):
        # The sprite has to be moving in the same
        # direction as the offset. If its being pushed,
        # it will have already been pushed and "come
        # to a rest" so its _last_ movement is needed.
        down, right = self.offset
        last_hmove, last_vmove = sprite.last_hv
        last_hmove = 1 if last_hmove > 0 else -1 if last_hmove < 0 else 1
        last_vmove = 1 if last_vmove > 0 else -1 if last_vmove < 0 else 1
        hmove, vmove = sprite.hmove, sprite.vmove
        if (down in (vmove, last_vmove) and down) \
            or (right in (hmove, last_hmove) and right):
            leaving_area.remove(sprite)
            self.to.add(sprite)
            sprite.boundtop = sprite.boundrect.top + down
            sprite.rect.left = sprite.boundrect.left + right

    @classmethod
    def connect(cls, area1, area2):
        """Determine the orientation of two areas and make
        a pair of portals between them.

        Refuses if the areas are not touching.
        """

        if area1.top + area1.height == area2.top:
            cls._connect_vertical(area1, area2)
        elif area1.top == area2.top + area2.height:
            cls._connect_vertical(area2, area1)
        elif area1.left + area1.width == area2.left:
            cls._connect_horizontal(area1, area2)
        elif area1.left == area2.left + area2.width:
            cls._connect_horizontal(area2, area1)
        else:
            raise PlacementError("Could not find touching sides to create portal on.")

    @classmethod
    def _connect_vertical(cls, area1, area2):
        # area1 has to be on top
        assert area1.top != area2.top
        if area1.top > area2.top:
            return cls._connect_vertical(area2, area1)

        # When connecting vertical areas, the bottom area needs
        # to overlap this area to make room for the sprite. The
        # overlap will be invisible.
        area2.top -= 50
        area2.height += 50
        for sprite in area2:
            sprite.rect.top += 50

        portal_left = max(area1.left, area2.left)
        portal_width = min(area1.width, area2.width)

        p1 = area1.create_sprite(Portal,
                            topleft=(area1.height,
                                     portal_left - area1.left),
                            to=area2,
                            offset=(1, 0),
                            height=1, width=portal_width)

        p2 = area2.create_sprite(Portal,
                            topleft=(0, portal_left),
                            to=area1,
                            offset=(-1, 0),
                            height=1, width=portal_width)

        area1.neighbors.add(area2)
        area2.neighbors.add(area1)
        return p1, p2

    @classmethod
    def _connect_horizontal(cls, area1, area2):
        # area1 has to be on left
        assert area1.left != area2.left
        if area1.left > area2.left:
            return cls._connect_horizontal(area2, area1)

        height = area2.height

        # When connecting horizontal areas, the right area needs
        # to overlap this area to make room for the sprite. The
        # overlap will be invisible.
        area2.left -= 50
        area2.width += 50
        for sprite in area2:
            sprite.rect.left += 50

        portal_top = max(area1.top, area2.top)
        portal_height = min(area1.top + area1.height, area2.top + area2.height) - portal_top

        p1 = area1.create_sprite(Portal,
                            topleft=(portal_top - area1.top,
                                     area2.left - area1.left + 49),
                            to=area2,
                            offset=(0, 1),
                            height=portal_height, width=1)
        p2 = area2.create_sprite(Portal,
                            topleft=(portal_top - area2.top, 0),
                            to=area1,
                            offset=(0, -1),
                            height=portal_height, width=1)

        area1.neighbors.add(area2)
        area2.neighbors.add(area1)
        return p1, p2
