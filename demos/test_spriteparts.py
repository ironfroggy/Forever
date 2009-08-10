from foreverdrive.base import ForeverMain
from foreverdrive.modes.scrolling import ScrollingMode
from foreverdrive.area import AreaManager
from foreverdrive.sprite import Sprite, SolidSprite, FacingSprite, CloudSprite, ImmovableSprite, Player
from foreverdrive.events import Entering, CancelEvent

def report(event):
    print event.sprite.name, "entered", event.entered.name            

objects = []

class AreaManagingMode(ScrollingMode):

    def __init__(self, *args, **kwargs):
        super(AreaManagingMode, self).__init__(*args, **kwargs)
        self.areas = AreaManager(self)

    def first_entering(self):
        area = self.areas.new_areas([
            ((100, 100), (6, 6), None, None)
            ])[0]
        self.area = area

        sprite = area.create_sprite(
            Player,
            topleft=(300, 100),
            height=25,
            imagename="default_player",
            name="player")
        sprite.register_listeners(self.game.mode)
        self.player = sprite

        sprite.grow_part((-25, 0), "default_player")

        self.make_cylinder(0, 0)
        self.make_cylinder(75, 150)
        self.make_cylinder(25, 50)
        self.make_cylinder(0, 200)

    def make_cylinder(self, x, y):
        obj = self.area.create_sprite(
            SolidSprite,
            topleft=(x, y),
            height=30,
            image_path="default_oildrum",
            name="block")


def main():
    game = ForeverMain(initmode=AreaManagingMode)
    game.run()

if __name__ == '__main__':
    main()
