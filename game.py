import shelve, pickle, pygame, math, time
from common import Initialiser

class Game:
    def __init__(self, screen, config, current_level=None):
        self.current_level = current_level
        self.scale = 1/9.0
        self.config = config
        self.x_update, self.y_update = (False, False)
        if self.current_level:
            self.load_level(screen, num=current_level)

    def image_init(self, screen):
        self.images = {}
        for key, image in self.current_level.images.items():
            image = pygame.image.load(image)
            size = tuple([self.current_level.size]*2)
            image = pygame.transform.scale(image, size)
            self.images[key] = image

    def display(self, screen):
        level = self.current_level.level
        [[screen.blit(self.images[block.image], block.rect.move(self.current_level.level_offset)) for block in row] for row in level]

    def centering(self, level, screen, init=False):
        screen_x, screen_y = screen.get_size()
        if not init:
            offset_x, offset_y = self.current_level.level_offset
            player_pos = self.player.rect.topleft
        else:
            player_pos = [((len(level)+self.current_level.spawn[0])*screen_x),
                          ((len(level)+self.current_level.spawn[1])*screen_y)]
        if init:
            if len(level[0])*self.scale*screen_y < screen.get_size()[0]:
                level_x = (len(level[0]))*self.scale*screen_y
                offset_x = int((screen_x-level_x)/2)
            else:
                self.x_update = True
        if self.x_update:
            level_x = (len(level)+self.current_level.spawn[0])*self.scale*screen_x 
        if init:
            if len(level)*self.scale*screen_y < screen.get_size()[1]:
                level_y = len(level)*self.scale*screen_y * self.scale
                offset_y = int((screen_y-level_y)/2)
            else:
                self.y_update=True
        if self.y_update:
            offset_y = ((screen_y/2)-player_pos[1])
        return (offset_x, offset_y)

    def position_format(self, screen, player_image=None):
        level = self.current_level.level
        block_size = int(screen.get_size()[1]*self.scale)

        position = (0, 0)

        for row in level:
            for block in row:
                block.set_rect(position, tuple([block_size]*2))
                position = (position[0]+block_size, position[1])
            position = (0, position[1]+block_size)

        self.current_level.level = level
        self.current_level.size = block_size

    def load_level(self, screen, level=None, num=None):
        if num:
            with open('Levels/level'+str(num)+'.pkl', 'rb') as input:
                self.current_level = pickle.load(input)
        else:
            self.current_level = level
        self.x_update = False
        self.y_update = False
        screen_x, screen_y = screen.get_size()

        player_pos = ((self.current_level.spawn[0]*self.scale*screen_x), (self.current_level.spawn[1]*self.scale*screen_y))
        player_image = pygame.image.load('Images/player.png')

        self.current_level.level_offset = self.centering(self.current_level.level, screen, True)
        self.position_format(screen, player_image)
        self.image_init(screen)
        self.player = Player(self.config, player_image, self.current_level, player_pos, int(self.current_level.size/5))

    def run(self, events, screen):
        screen.fill((0, 0, 0))
        if self.x_update or self.y_update:
            self.current_level.level_offset = self.centering(self.current_level.level, screen)
        self.display(screen)
        self.player.run(screen, events, self.config, self.current_level.level_offset)
        return screen, None

class Player:
    def __init__(self, config, image, level, pos, size):
        self.set_rect(pos, tuple([size]*2))
        self.size = size
        self.level = level
        self.velocity = (0, 0)
        self.accelaration = (0, 0)
        self.terminal = config.terminal
        self.standing = False
        self.image = pygame.transform.scale(image, (size, size))

    def set_rect(self, pos, size):
        self.rect = pygame.Rect(pos, size)

    def movement(self, events, config):
        self.accelaration = (self.accelaration[0], config.gravity)
        if events.current_event.type == pygame.KEYDOWN:
            for event in events.current_events:
                if event.key == pygame.K_LEFT:
                    self.accelaration = (-config.speed, self.accelaration[1])
                elif event.key == pygame.K_RIGHT:
                    self.accelaration = (config.speed, self.accelaration[1])
                elif event.key == pygame.K_UP and self.standing:
                    self.velocity = (self.accelaration[0], -config.jump)
        elif self.velocity[0] and events.current_event.type == pygame.KEYUP:
            for event in events.current_events:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.velocity = (0, self.velocity[1])
                    self.accelaration = (0, self.accelaration[1])
        self.velocity = tuple([x+y  if abs(x+y) < self.terminal else x for x, y in zip(self.velocity, self.accelaration)])
        self.rect, output1 = self.collision_detect(self.rect.move((math.ceil(self.velocity[0]), 0)), 'x')
        self.rect, output2 = self.collision_detect(self.rect.move((0, math.ceil(self.velocity[1]))), 'y')
        self.standing = False
        if output2 == 'standing':
            self.standing = True
            self.velocity = (self.velocity[0], 0)

    def collision_detect(self, pos, direction):
        if direction == 'x':       y_point = pos[1]+(pos[3]/2)
        elif self.velocity[1] < 0: y_point = pos[1]
        else:                      y_point = pos[1]+pos[3]

        if direction == 'y':       x_point = pos[0]+(pos[2]/2)
        elif self.velocity[0] < 0: x_point = pos[0]
        else:                      x_point = pos[0]+pos[2]

        row = math.ceil((y_point)/self.level.size)-1
        column = math.ceil((x_point)/self.level.size)-1
        if direction == 'x':
            return self.level.level[row][column].x_collide(self.rect, self.velocity[0])
        if direction == 'y':
            return self.level.level[row][column].y_collide(self.rect, self.velocity[1])

    def run(self, screen, events, config, offset):
        self.movement(events, config)
        screen.blit(self.image, self.rect.move(offset))

class Block:
    def __init__(self, image):
        self.image = image

    def set_rect(self, pos, size):
        self.rect = pygame.Rect(pos, size)

class Air_Block(Block):
    def x_collide(self, startpos, velocity):
        return startpos.move((velocity, 0)), None

    def y_collide(self, startpos, velocity):
        return startpos.move((0,velocity)), None

class Normal_Block(Block):
    def x_collide(self, startpos, speed):
        endpos = startpos
        x_resize = pygame.Rect(self.rect[0]-1, self.rect[1], self.rect[2]+2, self.rect[3])
        if speed > 0 and x_resize.colliderect(startpos):
            endpos[0] = self.rect[0]-startpos[2]
        elif speed < 0 and x_resize.colliderect(startpos):
            endpos[0] = self.rect[0]+self.rect[2]
        else:
            endpos = endpos.move((speed, 0))
        return endpos, None

    def y_collide(self, startpos, speed):
        output = None
        endpos = startpos
        y_resize = pygame.Rect(self.rect[0], self.rect[1]-5, self.rect[2], self.rect[3]+10)
        if speed < 0 and y_resize.colliderect(startpos):
            endpos[1] = self.rect[1]+self.rect[3]
        elif speed > 0 and y_resize.colliderect(startpos):
            endpos[1] = self.rect[1]-startpos[3]
            output = 'standing'
        else:
            endpos = endpos.move((0, speed))
        return endpos, output

if __name__ == "__main__":
    WIDTH, HEIGHT = 1500, 900

    INIT = Initialiser()
    INIT.level_init()

    pygame.display.init()
    pygame.font.init()
    pygame.image.get_extended()
    infoObject = pygame.display.Info()

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
 
    GAME = Game(SCREEN, None, 1)

    while True:
        GAME.run(None, SCREEN)
        pygame.display.update()
