import pygame
from itertools import chain
from common import Button
from common import MenuTemplate

class MainMenu(MenuTemplate):
    def __init__(self, screen, first_play=True):
        self.image_init()
        self.button_init(first_play, screen)

    def button_init(self, first_play, screen):
        """initialises all the buttons that will be displayed on the screen"""
        screen_size = screen.get_size()
        uniform_size = self.size_ref(1/4.0, screen_size)

        x_pos = int((screen_size[0] - uniform_size[0])/2)
        y_space = int(((screen_size[1])-(3*uniform_size[1]))/4)

        pos = (x_pos, y_space)

        if first_play:
            game_label = "Begin"
        else:
            game_label = "Continue"
        self.game = Button(pos, uniform_size, game_label, self.images)
        pos = (x_pos, pos[1]+y_space+uniform_size[1])
        self.options = Button(pos, uniform_size, 'Options', self.images)
        pos = (x_pos, pos[1]+y_space+uniform_size[1])
        self.quit = Button(pos, uniform_size, 'Quit', self.images)
        self.buttons = (self.game, self.options, self.quit)

    def run(self, events, screen):
        output = list(chain(*[button.run(events, screen)[:-1] for button in self.buttons]))

        return screen, output

if __name__ == "__main__":
    from common import standard_menu_unit_test
    standard_menu_unit_test(MainMenu)
