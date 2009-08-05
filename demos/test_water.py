from foreverdrive.base import ForeverMain
from foreverdrive.modes.scrolling import ScrollingMode
from foreverdrive.area import AreaManager
from foreverdrive.sprite import Sprite, SolidSprite, FacingSprite, CloudSprite, ImmovableSprite
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
            ((125, 25), (6, 6), None, None)
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
    
        #self.area.add(sprite)

        for y in range(4):
            for x in range(4):
                obstruction = area.create_sprite(
                    CloudSprite,
                    topleft=(0, 0),
                    height=50,
                    image_path="default_cloud.png",
                    name="water %d" % (x,))
                #obstruction.image.fill((x*(20+(y%5)), x*(20+(y%3)), x*(20+(y%4)), 100))
                objects.append(obstruction)
                obstruction.boundrect.top += 10
                obstruction.boundrect.left += 10
                obstruction.boundrect.width -= 10
                obstruction.boundrect.height -= 10
                obstruction.pressure = 0.0005

        self.make_cylinder(100, 50)
        self.make_cylinder(100, 75)
        self.make_cylinder(100, 100)
        self.make_cylinder(75, 100)
        self.make_cylinder(50, 100)

        obj = area.create_sprite(
            SolidSprite,
            topleft=(150, 0),
            height=50,
            image_path="default_obstruction.png",
            name="block")
            #obstruction.show_bounds()

    def make_cylinder(self, x, y):
        obj = self.area.create_sprite(
            ImmovableSprite,
            topleft=(x, y+25),
            height=50,
            image_path="default_obstruction.png",
            name="block")
            #obstruction.show_bounds()


import random
class TestMain(ForeverMain):
    def tick(self, tick):
        return
        for obj in objects:
            obj.vmove = 0.8
            if random.randint(0, 100) > 99:
                obj.hmove = random.choice(xrange(-1, 2))
                obj.vmove = -0.5
            else:
                obj.hmove = 0

def main():
    game = TestMain(initmode=AreaManagingMode)
    game.run()

if __name__ == '__main__':
    main()
