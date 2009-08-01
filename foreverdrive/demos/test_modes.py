import pygame
from pygame.locals import *

from foreverdrive.base import ForeverMain, Mode
from foreverdrive.sprite import Sprite

def main():
    game = ForeverMain()
    sprite = Sprite()
    game.listen_arrows(sprite.handle_event)
    group = pygame.sprite.RenderUpdates()
    group.add(sprite)
    game.groups.append(group)

    pause = Mode()
    game.modes['pause'] = pause
    def enter_pause(event):
        game.set_mode('pause')
    def leave_pause(event):
        game.set_mode('init')
    game.mode.listen(enter_pause, KEYUP, K_p)
    pause.listen(leave_pause, KEYUP, K_p)

    def reset_movement():
        sprite.hmove = 0
        sprite.vmove = 0
    game.mode.entering = reset_movement

    game.run()

if __name__ == "__main__":
    main()
