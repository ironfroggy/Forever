from foreverdrive.errors import PlacementError
from foreverdrive.area import BoundArea
from foreverdrive.sprite.portal import Portal

class AreaManager(object):
    """Manages multiple areas and portals between them."""

    def __init__(self, mode, spriteset=None, default_area_class=BoundArea):
        self.spriteset = spriteset
        self.mode = mode
        self.areas = []
        self.namedareas = {}
        self.default_area_class = default_area_class

    def __iter__(self):
        return iter(self.areas)

    def add(self, area):
        self.mode.groups.append(area)
        self.areas.append(area)
        self.namedareas[area.name] = area
        area.manager = self

    def new_area(self,
                 (top, left),
                 (tiles_wide, tiles_tall),
                 ):
        area = self.default_area_class(
            self.spriteset,
            size=(tiles_wide, tiles_tall),
            topleft=(top, left),
            mode=self.mode)
        self.add(area)
        return area

    def new_areas(self, dimensions):
        areas = []
        for (topleft, size) in dimensions:
            area = self.new_area(topleft, size)
            areas.append(area)
        return areas

    def connect_all(self):
        for area1 in self.areas:
            for area2 in self.areas:
                if area1 in area2.neighbors:
                    continue
                try:
                    Portal.connect(area1, area2)
                except PlacementError:
                    continue

    def decorate_all(self):
        """Calls the 'decorate' method of each area with
        it, which does things like add walls.
        """

        for area in self.areas:
            try:
                decorate = area.decorate
            except AttributeError:
                continue
            else:
                decorate()
                
