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
        player_image = pygame.image.load('Images/player.png')
        self.player = Player(player_image, (100,100,20,20))
        self.image_init(screen)

    def run(self, events, screen):
        screen.fill((0, 0, 0))
        self.display(screen)
        self.player.run(screen, events)
        return screen, None

class Player:
    def __init__(self, image, rect):
        self.rect = pygame.Rect(rect)
        self.velocity = (0, 0)
        self.image = pygame.transform.scale(image, rect[2:])

    def movement(self, events):
        if events.current_event.type == pygame.KEYDOWN:
            if events.current_event.key == pygame.K_LEFT:
                self.velocity = (-5, self.velocity[1])
            elif events.current_event.key == pygame.K_RIGHT:
                self.velocity = (5, self.velocity[1])
        else:
            self.velocity = (0, self.velocity[1])
        self.rect = self.rect.move(self.velocity)

    def run(self, screen, events):
        self.movement(events)
        screen.blit(self.image, self.rect)

class Block:
    def __init__(self, size):
        self.rect = pygame.Rect((0, 0), size)

class Air_Block(Block):
    pass

class Normal_Block(Block):
    pass

if __name__ == "__main__":
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
        GAME.run(None, SCREEN)
        pygame.display.update()
