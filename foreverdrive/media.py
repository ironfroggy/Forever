import pygame
from os.path import join as pathjoin

extension = {
    'sprite': 'png',
}

class Media(object):
    """Manages loading media from template and pallette sets."""

    def __init__(self, basedir="foreverdrive/media"):
        self.basedir = basedir

    def open(self, media_type, theme, palette, state=None):
        """

        sprite: graveyard - boneboy_head right
        """
        path = pathjoin(self.basedir, theme, palette)
        if state:
            path = '_'.join((path, state))
        return '.'.join((path, extension[media_type]))

media_manager = Media()

class SpriteSet(object):

    path_pattern = "foreverdrive/media/%(spriteset)s/%(slotname)s.png"

    def __init__(self, name):
        self.name = name

    def getGraphicForSlot(self, slotgroup, slotname):
        return self.path_pattern % {'spriteset':self.name, 'slotname': slotname}

    def load(self, slotgroup, slotname):
        if slotgroup is not None:
            slotname = '_'.join((slotgroup, slotname))
        try:
            return self._load(self.name, slotname)
        except:
            try:
                return self._load("defaults", slotname)
            except:
                return self._load("defaults", "default_tile")


    def _load(self, setname, slotname):
        f = media_manager.open('sprite', setname, slotname)
        return pygame.image.load(f).convert_alpha()

default_spriteset = SpriteSet("defaults")
