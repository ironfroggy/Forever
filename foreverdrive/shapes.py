import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, color, initial_position):

        # All sprite classes should extend pygame.sprite.Sprite. This
        # gives you several important internal methods that you probably
        # don't need or want to write yourself. Even if you do rewrite
        # the internal methods, you should extend Sprite, so things like
        # isinstance(obj, pygame.sprite.Sprite) return true on it.
        pygame.sprite.Sprite.__init__(self)
      
        # Create the image that will be displayed and fill it with the
        # right color.
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position

class UpDownBox(pygame.sprite.Sprite):
    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.going_down = True # Start going downwards
        self.next_update_time = 0 # update() hasn't been called yet.

    def update(self, current_time, bottom):
        # Update every 10 milliseconds = 1/100th of a second.
        if self.next_update_time < current_time:

            # If we're at the top or bottom of the screen, switch directions.
            if self.rect.bottom == bottom - 1: self.going_down = False
            elif self.rect.top == 0: self.going_down = True
     
            # Move our position up or down by one pixel
            if self.going_down: self.rect.top += 1
            else: self.rect.top -= 1

            self.next_update_time = current_time + 10

class MovingBox(Box):
    hmove = 0
    vmove = 0
    lastmove = 0
    speed = 15.0

    def update(self, current_time):
        if (current_time - self.lastmove) > self.speed:
            self.rect.top += self.vmove
            self.rect.left += self.hmove
            self.lastmove = current_time

    def handle_event(self, event):
        if event.type == pygame.locals.KEYDOWN:
            change = 1
        elif event.type == pygame.locals.KEYUP:
            change = -1

        if event.key == pygame.locals.K_UP:
            self.vmove -= change
        elif event.key == pygame.locals.K_DOWN:
            self.vmove += change
        elif event.key == pygame.locals.K_LEFT:
            self.hmove -= change
        elif event.key == pygame.locals.K_RIGHT:
            self.hmove += change

