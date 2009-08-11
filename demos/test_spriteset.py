from foreverdrive.base import ForeverMain
from foreverdrive.modes.scrolling import ScrollingMode
from foreverdrive.area import AreaManager
from foreverdrive.sprite import Sprite, SolidSprite, FacingSprite, CloudSprite, ImmovableSprite, Player
from foreverdrive.events import Entering, CancelEvent
from foreverdrive.media import SpriteSet

class AreaManagingMode(ScrollingMode):

    def __init__(self, *args, **kwargs):
        super(AreaManagingMode, self).__init__(*args, **kwargs)
        self.areas = AreaManager(self)

    def first_entering(self):
        area = self.areas.new_areas([
            ((100, 100), (6, 6)),
            ((400, 200), (3, 8)),
            ])[0]
        self.areas.connect_all()
        self.area = area

        player_sprite_set = SpriteSet("defaults")

        sprite = area.create_sprite(
            Player,
            topleft=(200, 100),
            height=25,
            spriteset=player_sprite_set,
            name="player")
        sprite.register_listeners(self)
        self.player = sprite

        sprite.grow_part((-25, 0), 'head')

        self.make_cylinder(0, 0)
        self.make_cylinder(75, 150)
        self.make_cylinder(25, 50)
        self.make_cylinder(0, 200)

        super(AreaManagingMode, self).first_entering()

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
