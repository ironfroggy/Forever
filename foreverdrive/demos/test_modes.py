import pygame
from pygame.locals import *

from foreverdrive.base import ForeverMain, Mode, PAUSE
from foreverdrive.sprite import Sprite

def main():
    game = ForeverMain()
    sprite = Sprite()
    game.listen_arrows(sprite.handle_event)
    game.mode.listen_pause(sprite.handle_event)
    group = pygame.sprite.RenderUpdates()
    group.add(sprite)
    game.groups.append(group)

    pause = Mode()
    game.modes['pause'] = pause
    def enter_pause(event):
        game.mode.route(PAUSE)
        game.set_mode('pause')
    def leave_pause(event):
        game.set_mode('init')
    game.mode.listen(enter_pause, KEYUP, K_p)
    pause.listen(leave_pause, KEYUP, K_p)

    game.run()

if __name__ == "__main__":
    main()
