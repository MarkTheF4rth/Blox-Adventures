import pygame
from itertools import chain
from common import Button
from common import MenuTemplate
from common import Initialiser

class OptionMenu(MenuTemplate, Initialiser):
    def button_init(self, screen):
        sound = 'Off'
        if self.options['volume'] > 0:
            sound = 'On'
        screen_size = screen.get_size()
        back_pos = (int(screen_size[0]*(4/6.0)), int(screen_size[1]*(5/6.0)))
        fullscreen_pos = (int(screen_size[0]*(1/20.0)), int(screen_size[1]*(1/3.0)))
        sound_pos = (int(screen_size[0]*(2/5.0)), int(screen_size[1]*1/20.0))
        
        self.sound = Button(sound_pos, self.size_ref(1/8.0, screen_size, 2), sound, function='sound_toggle')
        self.back = Button(back_pos, self.size_ref(1/8.0, screen_size), 'Back', function='mainmenu')
        self.fullscreen = Button(fullscreen_pos, self.size_ref(1/8.0, screen_size), 'Fullscreen')
        self.buttons = (self.back, self.fullscreen, self.sound)

    def run(self, events, screen):
        output = list(chain(*[button.run(events, screen)[:-1] for button in self.buttons]))

        return screen, output

if __name__ == "__main__":
    from common import standard_menu_unit_test
    standard_menu_unit_test(OptionMenu)
