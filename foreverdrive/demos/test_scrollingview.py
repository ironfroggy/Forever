from foreverdrive.demos.test_boundarea import *

class Window(object):
    rect = pygame.Rect(100, 100, 300, 300)

class ScrollingMode(TestMode):

    area_size = (10, 10)

    def first_entering(self):
        super(ScrollingMode, self).first_entering()

        self.player.game = self.game
        self.listen_move(self.player_moved)

    def player_moved(self, event):
        rect = event.rect
        window = Window()

        bottom_over = (rect.top + rect.height) - (window.rect.top + window.rect.height)
        if bottom_over > 0:
            self.area.top -= bottom_over
        else:
            top_under = window.rect.top - rect.top
            if top_under > 0:
                self.area.top += top_under

        right_over = (rect.left + rect.width) - (window.rect.left + window.rect.width)
        if right_over > 0:
            self.area.left -= right_over
        else:
            left_under = window.rect.left - rect.left
            if left_under > 0:
                self.area.left += left_under

def main():
    game = ForeverMain(initmode=ScrollingMode)
    game.run()

if __name__ == '__main__':
    main()
