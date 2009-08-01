from pygame.sprite import Sprite, RenderUpdates

class DirtySprite(Sprite):
  def __init__(self):
    Sprite.__init__(self)
    self.dirty = True

class RenderDirty(RenderUpdates):
  def draw(self, surface):
    dirty = self.lostsprites
    self.lostsprites = []
    for s, r in self.spritedict.items():
      if not s.dirty:
        continue

      s.dirty = False
      newrect = surface.blit(s.image, s.rect)
      if r is 0:
        dirty.append(newrect)
      else:
        if newrect.colliderect(r):
          dirty.append(newrect.union(r))
        else:
          dirty.append(newrect)
          dirty.append(r)
      spritedict[s] = newrect
    return dirty
