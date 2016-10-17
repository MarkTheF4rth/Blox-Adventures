import shelve, pickle, pygame
from common import Initialiser

class Game:
    def __init__(self, screen, current_level=None):
        self.current_level = current_level
        self.scale = 1/9.0
        if self.current_level:
            self.load_level(current_level, screen)

    def image_init(self, screen):
        self.images = {}
        size = tuple([int(screen.get_size()[1]*self.scale)]*2)
        for key, image in self.current_level.images.items():
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, size)
            self.images[key] = image

    def centering(self, level, screen):
        screen_x, screen_y = screen.get_size()
        level_x = (len(level[0]))*self.scale*screen_y
        level_y = len(level)*self.scale*screen_y
        return ((screen_x-level_x)/2, (screen_y-level_y)/2)

    def display(self, screen):
        level = self.current_level.level
        offset_x, offset_y = self.centering(level, screen)
        position = (offset_x, offset_y)
        offset = screen.get_size()[1]*self.scale
        for row in level:
            for image in row:
                screen.blit(self.images[image], position)
                position = (position[0]+offset, position[1])
            position = (offset_x, position[1]+offset)

    def load_level(self, num, screen):
        with open('Levels/level'+str(num)+'.pkl', 'rb') as input:
            self.current_level = pickle.load(input)
        self.image_init(screen)

    def run(self, events,  screen):
        self.display(screen)
        return screen, None

if __name__ == "__main__":
    import pygame
    WIDTH, HEIGHT = 1500, 900

    INIT = Initialiser()
    INIT.level_init()

    pygame.display.init()
    pygame.font.init()
    pygame.image.get_extended()
    infoObject = pygame.display.Info()

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
 
    GAME = Game(SCREEN, 1)

    while True:
        GAME.display(SCREEN)
        pygame.display.update()
