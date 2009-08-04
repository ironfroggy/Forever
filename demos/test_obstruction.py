from foreverdrive.base import ForeverMain
from foreverdrive.modes import Mode
from foreverdrive.area import AreaManager
from foreverdrive.sprite import Sprite, SolidSprite, FacingSprite
from foreverdrive.events import Entering, CancelEvent

def report(event):
    print event.sprite.name, "entered", event.entered.name            

class AreaManagingMode(Mode):

    def __init__(self, *args, **kwargs):
        super(AreaManagingMode, self).__init__(*args, **kwargs)
        self.areas = AreaManager(self)

    def first_entering(self):
        area = self.areas.new_areas([
            ((75, 75), (6, 6), None, None)
            ])[0]
        self.area = area

        sprite = area.create_sprite(
            FacingSprite,
            topleft=(self.area.top+50,
                     self.area.left+50),
            height=15,
            imagename="default_player",
            name="player")
        sprite.register_listeners(self.game.mode)
        self.player = sprite
        sprite.show_bounds()
    
        self.area.add(sprite)

        for i, topleft in enumerate(((150, 150),
                        (50, 250),
                        (50, 50),
                        (300, 100), (300, 150), (300, 200),
                        (320, 250), (340, 300), (360, 350)
                        )):
            obstruction = area.create_sprite(
                SolidSprite,
                topleft=topleft,
                height=15,
                image_path="default_obstruction.png",
                name="block %d" % (i,))

            obstruction.show_bounds()


def main():
    game = ForeverMain(initmode=AreaManagingMode)
    game.run()

if __name__ == '__main__':
    main()
