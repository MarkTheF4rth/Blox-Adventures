import pygame, mainmenu, optionsmenu, time, common

class Run:
    def __init__(self, events):
        self.events = events
        self.screen_width = 1500
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.status = 'mainmenu'
        self.fullscreen = False #PLACEHOLDER, NEED OPTIONS SHELF
        self.volume = 100 # PLACEHOLDER FOR OPTIONS
        self.original_volume = 100 #PLACEHOLDER FOR OPTIONS
        self.status_types = ['mainmenu', 'options']
        self.initialise()

    def initialise(self):
        self.mainmenu = mainmenu.MainMenu(self.screen) #PLACEHOLDER: FIRST PLAY NEEDS TO BE SET
        self.options = optionsmenu.OptionMenu(self.volume, self.screen)

    def output_handler(self, output):
         if output[0] in self.status_types: 
            self.status = output[0]
            self.screen.fill((0, 0,0))
            self.events.click_timeout()
         else:
            getattr(self, 'handle_'+output[0])(*output[1:])
       

    def main_loop(self):
        while self.status != 'quit':
            self.events.event_update()
            self.screen, output = getattr(self, self.status).run(self.events, self.screen)
            if output:
                [self.output_handler(a) for a in output if a]
            pygame.display.update()

    def handle_fullscreen(self):
        info = pygame.display.Info()
        if not self.fullscreen:
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            self.fullscreen = True
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            self.fullscreen = False
        self.initialise()

    def handle_sound_toggle(self):
        if self.volume > 0:
            self.volume = 0
        else:
            self.volume = self.original_volume
        self.options.button_init(self.volume, self.screen)

    def handle_quit(self):
        self.status = 'quit'


if __name__ == "__main__":
    pygame.display.init()
    pygame.font.init()
    pygame.image.get_extended()

    EVENTS = common.Events(pygame.mouse.get_pos())
    RUN = Run(EVENTS)
    RUN.main_loop()
