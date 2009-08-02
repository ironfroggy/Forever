from foreverdrive.events import EventRouter
from foreverdrive.area import TileArea
from foreverdrive.events import Pause

class Mode(EventRouter):
    def __init__(self, game):
        super(Mode, self).__init__()
        self.game = game
        self.background = TileArea("default_tile.png",
                                   (10, 10))

        self.groups = []

    def first_entering(self):
        pass

    new = True
    def entering(self):
        if self.new:
            self.new = False
            self.first_entering()
        for group in self.groups:
            for sprite in group:
                try:
                    handle_event = sprite.handle_event
                except AttributeError:
                    pass
                else:
                    handle_event(Pause())

    def leaving(self):
        pass
