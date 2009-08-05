class Bound(object):
    def __init__(self, sprite):
        self.sprite = sprite
    @property
    def rect(self):
        return self.sprite.boundrect

    def __getattr__(self, name):
        return getattr(self.sprite, name)

class RectHolder(object):
    def __init__(self, rect):
        self.rect = rect
