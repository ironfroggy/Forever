from itertools import cycle

from foreverdrive.base import ForeverMain
from foreverdrive.modes import Mode
from foreverdrive.area import AreaManager
from foreverdrive.sprite import Sprite, PushableSprite, FacingSprite, SolidSprite

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
            topleft=(self.area.top+50, self.area.left),
            imagename="default_player",
            name="player")
        sprite.register_listeners(self.game.mode)
        self.player = sprite
        sprite.show_bounds()
    
        self.area.add(sprite)

        color = iter(cycle([(128, 128, 250, 128),
                            (128, 250, 128, 128),
                            (250, 128, 128, 128),
                            (50, 100, 200, 128),
                            (100, 50, 200, 128),
                            ])).next
        obstruction = area.create_sprite(
            SolidSprite,
            (100, 50),
            height = 50,
            image_path="default_obstruction.png")

        for i, topleft in enumerate([(150, 150),
                        (150, 200),
                        (50, 250),
                        (50, 50),
#                        (300, 100), (300, 150), (300, 200),
#                        (320, 250), (340, 300), (360, 350)
                        ]):
            obstruction = area.create_sprite(
                PushableSprite,
                topleft=topleft,
                height=50,
                image_path="default_obstruction.png",
                name="block " + str(i))
            obstruction.image.fill(color())

            #obstruction.show_bounds()


def main():
    game = ForeverMain(initmode=AreaManagingMode)
    game.run()

if __name__ == '__main__':
    main()
