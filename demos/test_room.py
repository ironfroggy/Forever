from foreverdrive.base import ForeverMain
from foreverdrive.modes.scrolling import ScrollingMode
from foreverdrive.area import AreaManager
from foreverdrive.area.room import Room
from foreverdrive.sprite import Sprite, SolidSprite, FacingSprite, CloudSprite, ImmovableSprite, Player
from foreverdrive.events import Entering, CancelEvent
from foreverdrive.media import SpriteSet

cottage_spriteset = SpriteSet("cottage")

class RoomTestMode(ScrollingMode):

    def __init__(self, *args, **kwargs):
        super(RoomTestMode, self).__init__(*args, **kwargs)
        self.areas = AreaManager(self, cottage_spriteset, Room)

    def first_entering(self):
        area = self.areas.new_areas([
            ((60, 60), (15, 15)),
            ])[0]
        self.areas.connect_all()
        self.areas.decorate_all()
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

        super(RoomTestMode, self).first_entering()

    def make_cylinder(self, x, y):
        obj = self.area.create_sprite(
            SolidSprite,
            topleft=(x, y),
            height=30,
            slotgroup="default", slotname="oildrum",
            name="block")


def main():
    game = ForeverMain(initmode=RoomTestMode)
    game.run()

if __name__ == '__main__':
    main()
