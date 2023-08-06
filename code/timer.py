from settings import *


class Timer:
    def __init__(self, duration, repeated=False, func=None):
        self.duration = duration
        self.repeated = repeated
        self.func = func

        self.start_time = None
        self.active = False

    def activate(self):
        self.start_time = pygame.time.get_ticks()
        self.active = True

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration and self.active:
            if self.func:
                self.func()

            # reset the timer
            self.deactivate()

            # if the timer is repeated, activate it again
            if self.repeated:
                self.activate()