import pygame, mainmenu, optionsmenu, game, time, common, os
from itertools import chain
from common import Initialiser
from common import StorageObj
from common import Button

class Run(Initialiser):
    def __init__(self, events):
        self.events = events
        self.screen_width = 1500
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.status = 'mainmenu'
        self.prompt_obj = None
        if not os.path.isfile('Config'):
            self.config_initialise()
        self.status_types = ['mainmenu', 'optionsmenu', 'game']
        self.initialise()

    def initialise(self):
        self.reader()
        self.mainmenu = mainmenu.MainMenu(self.screen)
        self.optionsmenu = optionsmenu.OptionMenu(self.screen)
        self.game = game.Game(self.screen, self.config, current_level=1)

    def output_handler(self, output):
        if output[0] in self.status_types: 
           self.status = output[0]
           self.screen.fill((0, 0,0))
           self.events.click_timeout()
        else:
           getattr(self, 'handle_'+output[0])(*output[1:])

    def run_prompt(self):
        output = list(chain(*[button.run(self.events, self.screen)[:-1] for button in self.prompt_obj.buttons]))
        for a in output:
            if a:
                if self.prompt_obj.behaviour[a[0]]:
                    self.output_handler([self.prompt_obj.behaviour[a[0]]])
                self.prompt_obj = None

    def main_loop(self):
        while self.status != 'quit':
            self.events.event_update()
            if not self.prompt_obj:
                self.screen, output = getattr(self, self.status).run(self.events, self.screen)
                if output:
                    [self.output_handler(a) for a in output if a]
            else:
                self.run_prompt()
            pygame.display.update()

    def handle_prompt_menu(self, text, options):
        self.prompt_obj = StorageObj()
        pygame.draw.rect(self.screen, (50, 50, 50), (100, 100, self.screen_width-200, self.screen_height-200))
        x, y = 250, self.screen_height/2
        x_interval = int((self.screen_width-500)/len(options))
        self.prompt_obj.buttons = []
        font = pygame.font.SysFont(None, 100)
        text = font.render(text, True, (0, 0, 0))
        self.screen.blit(text, (150, 150))
        self.prompt_obj.behaviour = {}
        for button_name, function in options.items():
            self.prompt_obj.buttons.append(Button((x, y), (x_interval-50, 150), button_name))
            self.prompt_obj.behaviour.update({button_name.lower():function})
            x += x_interval

    def handle_fullscreen(self):
        info = pygame.display.Info()
        if not self.options['fullscreen']:
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            self.options['fullscreen'] = True
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            self.options['fullscreen'] = False
        self.initialise()

    def handle_sound_toggle(self):
        if self.options['volume'] > 0:
            self.options['volume'] = 0
        else:
            self.options['volume'] = self.options['original_volume']
        self.initialise()

    def handle_quit(self):
        self.status = 'quit'


if __name__ == "__main__":
    pygame.display.init()
    pygame.font.init()
    pygame.image.get_extended()

    EVENTS = common.Events(pygame.mouse.get_pos())
    RUN = Run(EVENTS)
    RUN.main_loop()
