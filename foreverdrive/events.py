class Movement(object):
    def __init__(self, player, movement):
        self.player = player
        self.rect = player.rect
        self.movement = movement

class Scroll(object):
    def __init__(self, window, movement):
        self.window = window
        self.x, self.y = movement
        print "scroll", movement
