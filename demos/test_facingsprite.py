from foreverdrive.base import ForeverMain
from foreverdrive.modes import Mode
from foreverdrive.area import AreaManager
from foreverdrive.sprite import FacingSprite

class TestMode(Mode):

    def __init__(self, *args, **kwargs):
        super(TestMode, self).__init__(*args, **kwargs)
        self.areas = AreaManager(self)

    def first_entering(self):
        area = self.areas.new_area((25, 25), (4, 8))
        self.areas.new_area((0, 0), (8, 4), relative_to=area.bottom_left)

        self.player = FacingSprite(imagename="default_player")
        area.add(self.player)
        self.game.listen_arrows(self.player.handle_event)

def main():
    game = ForeverMain(initmode=TestMode)
    game.run()

if __name__ == '__main__':
    main()
