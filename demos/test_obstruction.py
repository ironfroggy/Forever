from foreverdrive.base import ForeverMain
from foreverdrive.modes import Mode
from foreverdrive.area import AreaManager
from foreverdrive.sprite import Sprite, PerimeterSensoringMixin, FacingSprite
from foreverdrive.events import Entering

def report(event):
    print event.sprite.name, "entered", event.entered.name

class PerimeterSprite(PerimeterSensoringMixin, Sprite):
    def enter(self, area, sprite):
        super(PerimeterSprite, self).enter(area, sprite)
        if sprite.vmove < 0:
            sprite.move(-1)
        elif sprite.vmove > 0:
            sprite.move(-1)
            

class AreaManagingMode(Mode):

    def __init__(self, *args, **kwargs):
        super(AreaManagingMode, self).__init__(*args, **kwargs)
        self.areas = AreaManager(self)

    def first_entering(self):
        area = self.areas.new_areas([
            ((125, 125), (6, 6), None, None)
            ])[0]
        self.area = area

        sprite = FacingSprite(topleft=(self.area.top+50, self.area.left+50), imagename="default_player", area=self.area, name="player")
        sprite.register_listeners(self.game.mode)
        self.player = sprite
        sprite.show_bounds()
    
        self.area.add(sprite)

        obstruction = area.create_sprite(
            PerimeterSprite,
            topleft=(200, 100),
            bound_topleft=(80, 0),
            height=25,
            image_path="default_obstruction.png",
            name="block")

        obstruction.listen(report, Entering)
        obstruction.show_bounds()


def main():
    game = ForeverMain(initmode=AreaManagingMode)
    game.run()

if __name__ == '__main__':
    main()
