import pygame

class Button(object):
    def __init__(self, pos, size, label, images, status='normal'):
        """initialises button object"""
        self.pos = pos
        self.size = size
        self.label = label
        self.images = images
        self.status = status
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.colours = {
            'normal': (58, 45, 233),
            'active': (255, 255, 255), 
            'inactive': (0, 0, 0)}
        self.text_prep()

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

class MainMenu(Button):
    def __init__(self, first_play, screen):
        self.image_init()
        self.button_init(first_play, screen)

    def image_init(self):
        imagedir = 'Images'
        normal = pygame.image.load(imagedir+"/button_normal.png")
        active = pygame.image.load(imagedir+"/button_active.png")
        inactive = pygame.image.load(imagedir+"/button_inactive.png")
        self.images = (normal, active, inactive)

    def button_init(self, first_play, screen):
        """initialises all the buttons that will be displayed on the screen"""
        screen_size = screen.get_size()
        uniform_size_y = int(1/4 * screen_size[1])  # Find the size that y should be relative to the screen size
        uniform_size_x = int(uniform_size_y * 4)               # Create x value from that, ration 4:1 x:y
        uniform_size = (uniform_size_x, uniform_size_y)  # Put them together in a tuple

        x_pos = int((screen_size[0] - uniform_size_x)/2)
        y_space = int(((screen_size[1])-(3*uniform_size_y))/4)

        pos = (x_pos, y_space)

        if first_play:
            game_label = "Begin"
        else:
            game_label = "Continue"
        self.game = Button(pos, uniform_size, game_label, self.images)
        pos = (x_pos, pos[1]+y_space+uniform_size_y)
        self.options = Button(pos, uniform_size, 'Options', self.images)
        pos = (x_pos, pos[1]+y_space+uniform_size_y)
        self.quit = Button(pos, uniform_size, 'Quit', self.images)
        self.buttons = (self.game, self.options, self.quit)

    def run(self, events, screen):
        output = None
        for button in self.buttons:
            button.mouse_hover(events.mouse_pos)
            screen = button.draw(screen)

        if events.mouse_down[0]:
            for button in self.buttons:
                if button.status == 'active':
                    output = button.label.lower()

        return screen, output

class Events(object):
    def __init__(self, mouse_pos):
        self.mouse_pos = mouse_pos
        self.current_event = None


if __name__ == "__main__":

    WIDTH, HEIGHT = 1500, 900

    pygame.display.init()
    pygame.font.init()
    pygame.image.get_extended()
    infoObject = pygame.display.Info()


    FULLSCREEN = False
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    MAINMENU = MainMenu(True, SCREEN)
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
                MAINMENU.button_init(True, SCREEN)
                FULLSCREEN = not FULLSCREEN
            else:
                EVENTS.current_event = event

        EVENTS.mouse_pos = pygame.mouse.get_pos()
        EVENTS.mouse_down = pygame.mouse.get_pressed()
        SCREEN, OUTPUT = MAINMENU.run(EVENTS, SCREEN)
        if OUTPUT == 'quit':
            RUN = False
        pygame.display.update()
    pygame.quit()
