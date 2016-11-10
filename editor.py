import pygame
from common import Events
from common import Button
from common import Initialiser

class Block:
    def __init__(self, position, size):
        self.rect = pygame.Rect(position, size)

class Editor:
    def __init__(self, events):
        self.events = events(pygame.mouse.get_pos)
        self.screen_width, self.screen_height = 1500, 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.scale = 1/9.0
        self.level_images = {'empty':
        self.level = {}

    def display(self):
        endpos = self.screen.get_size()[1]
        offset = endpos*self.scale
        self.blocks = []
        for ypos in range(0,10):
            self.blocks.append([Block(offset*pos, ), 0])
            for xpos in range(0, 10):
                pygame.draw.line(self.screen, (255, 255, 255), (offset*pos, 0), (offset*pos, endpos), 5)

        

    def run(self):
        while True:
            self.events.event_update()
            self.display()
            pygame.display.flip()
        
if __name__ == "__main__":
    pygame.display.init()
    pygame.font.init()
    pygame.image.get_extended()

    EDITOR = Editor(Events)
    EDITOR.run()
