import pygame, sys
from common import Events
from common import Button
from common import Initialiser
from common import StorageObj
from game import Game

from game import AirBlock

class Block:
    def __init__(self, position, size):
        self.rect = pygame.Rect(position, size)

class Editor(Game):
    def __init__(self, events, level=None):
        self.events = events(pygame.mouse.get_pos)
        self.screen_width, self.screen_height = 1500, 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.scale = 1/9.0
        self.current_level = level
        if self.current_level:
            self.load_level(current_level, screen)
        else:
            print('Level not inputted, creating one')
            self.current_level = StorageObj()
            block = lambda : AirBlocka
            row = ['empty']*9
            self.current_level.spawn = (4, 4)
            self.current_level.level = [row]*9
            self.current_level.images = {'empty':'Images/emptyblock.png'}
            self.load_level(self.screen,level=self.current_level)
            self.image_init(self.screen)

    def run(self):
        while True:
            self.events.event_update()
            self.display(self.screen)
            pygame.display.flip()
        
if __name__ == "__main__":
    pygame.display.init()
    pygame.font.init()
    pygame.image.get_extended()

    EDITOR = Editor(Events, sys.argv[1:])
    EDITOR.run()
