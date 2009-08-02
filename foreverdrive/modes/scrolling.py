from foreverdrive.modes import Mode
from foreverdrive.events import Movement, Scroll
from foreverdrive.base import Window

class ScrollingMode(Mode):

    def first_entering(self):
        super(ScrollingMode, self).first_entering()

        self.player.game = self.game
        self.listen(self.player_moved, Movement)

    def player_moved(self, event):
        rect = event.rect
        window = Window()

        x = 0
        y = 0

        bottom_over = (rect.top + rect.height) - (window.rect.top + window.rect.height)
        if bottom_over > 0:
            self.area.top -= bottom_over
            y = -bottom_over
        else:
            top_under = window.rect.top - rect.top
            if top_under > 0:
                self.area.top += top_under
                y = top_under

        right_over = (rect.left + rect.width) - (window.rect.left + window.rect.width)
        if right_over > 0:
            self.area.left -= right_over
            x = -right_over
        else:
            left_under = window.rect.left - rect.left
            if left_under > 0:
                self.area.left += left_under
                x = left_under

        if x or y:
            self.route(Scroll(window, (x, y)))
