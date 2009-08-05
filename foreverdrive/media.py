from os.path import join as pathjoin

extension = {
    'sprite': 'png',
}

class Media(object):
    """Manages loading media from template and pallette sets."""

    def __init__(self, basedir="foreverdrive/media"):
        self.basedir = basedir

    def open(self, media_type, theme, pallette, state=None):
        """

        sprite: graveyard - boneboy_head right
        """
        path = pathjoin(self.basedir, theme, pallette)
        if state:
            path = '_'.join((path, state))
        return '.'.join((path, extension[media_type]))
