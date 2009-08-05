from foreverdrive.base import ForeverMain
from foreverdrive.modes import Mode
from foreverdrive.area import AreaManager
from foreverdrive.sprite import Sprite, SolidSprite, ImmovableSprite, FacingSprite
from foreverdrive.events import Entering, CancelEvent

def report(event):
    print event.sprite.name, "entered", event.entered.name            

objects = []

class AreaManagingMode(Mode):

    def __init__(self, *args, **kwargs):
        super(AreaManagingMode, self).__init__(*args, **kwargs)
        self.areas = AreaManager(self)

    def first_entering(self):
        area = self.areas.new_areas([
            ((0, 0), (10, 10), None, None)
            ])[0]
        self.area = area

        sprite = area.create_sprite(
            FacingSprite,
            topleft=(self.area.top+50,
                     self.area.left+50),
            height=50,
            imagename="default_player",
            name="player")
        sprite.speed *= 3
        sprite.register_listeners(self.game.mode)
        self.player = sprite
        #sprite.show_bounds()
    
        self.area.add(sprite)

        for i, topleft in enumerate(((150, 150),
                        (50, 250),
                        (50, 50),
                        (300, 100), (300, 150), (300, 200),
                        (320, 250), (340, 300), (360, 350)
                        )):
            cls = (SolidSprite, ImmovableSprite)[i % 2]
            obstruction = area.create_sprite(
                cls,
                topleft=topleft,
                height=50,
                image_path="default_tile.png",
                name="block %d" % (i,))
            obstruction.image.fill((i*(20+(i%5)), i*(20+(i%3)), i*(20+(i%4)), 128))
            objects.append(obstruction)

            #obstruction.show_bounds()


class TestMain(ForeverMain):
    def tick(self, tick):
        pass#objects[1].hmove = 0

def main():
    game = TestMain(initmode=AreaManagingMode)
    game.run()

if __name__ == '__main__':
    main()
