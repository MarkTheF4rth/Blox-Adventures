import pygame

class Events(object):
    def __init__(self, mouse_pos):
        self.mouse_pos = mouse_pos
        self.current_event = None

class Run:
    def __init__(self, events):
        self.events = events
        self.screen_width = 1500
        self.screen_height = 900
        self.screen = pygame.display.set_modea(self.screen_width, self.screen_height)

    def main_loop(self):
        

if __name__ == "__main__":
    pygame.display.init()
    pygame.font.init()
    pygame.image.get_extended()

    EVENTS = Events(pygame.mouse.get_pos())
    RUN = Run(EVENTS)
    Run.main_loop()
