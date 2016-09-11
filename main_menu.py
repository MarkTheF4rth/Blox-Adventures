#!/usr/bin/python3.5

import pygame

class Button(object):
    def __init__(self, pos, size, label, images, status='normal'):
        self.pos = pos
        self.size = size
        self.label = label
        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.images = images
        self.status = status

    def mouse_hover(self, mouse_pos):
        active = ['active', 'normal']
        if self.status in active:
            if self.rect.collidepoint(mouse_pos):
                self.status = 'active'
            else:
                self.status = 'normal'
    
    def draw(self, screen):
        status_ref = {'normal':0, 'active':1, 'inactive':2}
        image = self.images[status_ref[self.status]]
        image = pygame.transform.scale(image, self.size)
        screen.blit(image, self.pos)
        return screen

class MainMenu(Button):
    def __init__(self, first_play):
        self.image_init()
        self.button_init(first_play)

    def image_init(self):
        imagedir = 'Images'
        normal = pygame.image.load(imagedir+"/menu_button_normal.png")
        active = pygame.image.load(imagedir+"/menu_button_active.png")
        inactive = pygame.image.load(imagedir+"/menu_button_inactive.png")
        self.images = (normal, active, inactive)

    def button_init(self, first_play):
        uniform_size = (1000, 200)
        if first_play:
            game_label = "Begin"
        else:
            game_label = "Continue"
        self.game = Button((10, 10), uniform_size, game_label, self.images)
        self.options = Button((10, 210), uniform_size, 'options', self.images)
        self.quit = Button((10,410), uniform_size, 'quit', self.images)
        self.buttons = (self.game, self.options, self.quit)

    def run(self, events, screen):
        output = None
        for button in self.buttons:
            button.mouse_hover(events.mouse_pos)
            screen = button.draw(screen)

        if events.mouse_down[0]:
            for button in self.buttons:
                if button.status == 'active':
                    output = button.label

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

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    MAINMENU = MainMenu(True)
    EVENTS = Events(pygame.mouse.get_pos())

    RUN = True
    while RUN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
            else:
                EVENTS.current_event = event

        EVENTS.mouse_pos = pygame.mouse.get_pos()
        EVENTS.mouse_down = pygame.mouse.get_pressed()
        SCREEN, OUTPUT = MAINMENU.run(EVENTS, SCREEN)
        if OUTPUT == 'quit':
            RUN = False
        pygame.display.update()
    pygame.quit()
