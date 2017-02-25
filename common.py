import pygame, shelve, pickle

class Button(object):
    def __init__(self, pos, size, label, media=None, function=None, status='normal'):
        """initialises button object"""
        if media:
            self.images = media.images
            self.audio = media.audio
            self.colours = media.colours
        else:
            self.default_images()
        self.pos = pos
        self.size = size
        self.label = label
        self.function = function
        if not self.function:
            self.function = label.lower()
        self.status = status
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.text_prep()

    def default_images(self):
        self.media = StorageObj()
        self.image_dir = "Images"
        normal = pygame.image.load(self.image_dir+"/button_normal.png")
        active = pygame.image.load(self.image_dir+"/button_active.png")
        inactive = pygame.image.load(self.image_dir+"/button_inactive.png")
        self.images = (normal, active, inactive)
        self.colours = {
            'normal':(0, 0, 255),
            'active':(255, 255, 255),
            'inactive':(0, 0, 0)}

    def mouse_hover(self, mouse_pos):
        active = ['active', 'normal']
        if self.status in active:
            if self.rect.collidepoint(mouse_pos):
                self.status = 'active'
            else:
                self.status = 'normal'

    def text_prep(self):
        """prepares the text that will be put on top of the button"""
        self.text = {}

        font = pygame.font.SysFont(None, min(self.size))
        x_offset = ((self.rect[2]-font.size(self.label)[0])/2)
        y_offset = (self.rect[3]/6)
        normal_text = font.render(self.label, True, self.colours['normal'])
        active_text = font.render(self.label, True, self.colours['active'])
        inactive_text = font.render(self.label, True, self.colours['inactive'])
        text_ref = {"normal":normal_text, "active":active_text,
                "inactive":inactive_text}

        self.text['pos'] = (x_offset+self.pos[0], y_offset+self.pos[1])
        self.text['image'] = text_ref

    def draw(self, screen):
        status_ref = {'normal':0, 'active':1, 'inactive':2}
        image = self.images[status_ref[self.status]]
        image = pygame.transform.scale(image, self.size)
        screen.blit(image, self.pos)
        screen.blit(self.text['image'][self.status], self.text['pos'])
        return screen

    def run(self, events, screen):
        output = None
        self.mouse_hover(events.mouse_pos)
        if events.mouse_click and self.status == 'active':
            output = [self.function]

        return output, self.draw(screen)
 

class MenuTemplate:
    def __init__(self, screen):
        self.reader()
        self.button_init(screen)

    def sound_init(self):
        self.media.audio = None

    def size_ref(self, fraction, screen_size, scale=4):
        uniform_size_y = int(fraction * screen_size[1])
        uniform_size_x = int(uniform_size_y*scale)
        uniform_size = (uniform_size_x, uniform_size_y)
        return uniform_size

class Events(object):
    def __init__(self, mouse_pos):
        self.mouse_pos = mouse_pos
        self.mouse_down = (0, 0, 0)
        self.current_event = None
        self.timeout = 0
        self.mouse_click = False

    def click_timeout(self):
        self.timeout = 25
        self.mouse_click = False

    def event_update(self):
        if self.timeout == 0:
            LMB_down = self.mouse_down[0]
            self.mouse_click = False
            self.current_events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.handle_quit()
                else:
                    self.current_event = event
                    self.current_events.append(event)
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_down = pygame.mouse.get_pressed()
            if not LMB_down and self.mouse_down[0]:
                self.mouse_click = True
        else:
            self.timeout -= 1

class Initialiser:
    def config_initialise(self):
        config = open('Config', 'w')
        config.write('Format is: Option = <option>. order must be retained\n')
        config.write('First Play = 1\n')
        config.write('Image Directory = Images\n')
        config.write('Music Directory = Music\n')
        config.write('Gravity = 0.1\n')
        config.write('Terminal = 5\n')
        config.write('Jump = 5\n')
        config.write('Speed = 0.25')
        config.close()
        options = shelve.open('options')
        options['fullscreen'] = False
        options['volume'] = 100
        options['original_volume'] = 100

    def reader(self):
        config = open('Config', 'r')
        config.readline()
        self.first_play = int(config.readline().split('=')[1][1:].strip())
        self.image_dir = config.readline().split('=')[1][1:].strip()
        self.music_dir = config.readline().split('=')[1][1:].strip()
        self.config = StorageObj()
        self.config.gravity = float(config.readline().split('=')[1][1:].strip())
        self.config.terminal = int(config.readline().split('=')[1][1:].strip())
        self.config.jump = int(config.readline().split('=')[1][1:].strip())
        self.config.speed = float(config.readline().split('=')[1][1:].strip())
        config.close()
        self.options = shelve.open('options')

def standard_menu_unit_test(module):
    WIDTH, HEIGHT = 1500, 900

    pygame.display.init()
    pygame.font.init()
    pygame.image.get_extended()
    infoObject = pygame.display.Info()


    FULLSCREEN = False
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    MENU = module(SCREEN)
    EVENTS = Events(pygame.mouse.get_pos())

    RUN = True
    while RUN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                if not FULLSCREEN:
                    SCREEN = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
                else:
                    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
                MENU.button_init(True, SCREEN)
                FULLSCREEN = not FULLSCREEN
            else:
                EVENTS.current_event = event

        EVENTS.mouse_pos = pygame.mouse.get_pos()
        EVENTS.mouse_down = pygame.mouse.get_pressed()
        SCREEN, OUTPUT = MENU.run(EVENTS, SCREEN)
        if OUTPUT == 'quit':
            RUN = False
        pygame.display.update()
    pygame.quit()

class StorageObj:
    pass
