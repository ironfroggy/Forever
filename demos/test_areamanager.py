from foreverdrive.base import ForeverMain
from foreverdrive.modes import Mode
from foreverdrive.area import AreaManager
from foreverdrive.sprite import FacingSprite, SolidSprite

class AreaManagingMode(Mode):

    def __init__(self, *args, **kwargs):
        super(AreaManagingMode, self).__init__(*args, **kwargs)
        self.areas = AreaManager(self)

    def first_entering(self):
        self.area = self.areas.new_areas([
            ((75, 75), (3, 6)),
#            ((50, 175), (4, 4)),
#            ((-150, 100), (5, 1)),
#            ((-125, 50), (2, 2)),
            ])[0]
        self.areas.connect_all()

        sprite = self.area.create_sprite(
            FacingSprite,
            topleft=(self.area.top+50, self.area.left+50),
            imagename="default_player",
            height=25,
            name="player")
        sprite.register_listeners(self.game.mode)
        self.player = sprite
    
        self.area.add(sprite)
        self.make_cylinder(200, 50)

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
