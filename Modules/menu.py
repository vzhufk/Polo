# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 11.02.2017
import pygame

import font
import sprite
import surface
import varibles

position = (0.4 * varibles.screen_resolution[0], 0.3 * varibles.screen_resolution[1])
size = (0.2 * varibles.screen_resolution[0], 0.4 * varibles.screen_resolution[1])

color = (183, 183, 183)
sec_color = (106, 106, 106)

option_size = (160, 60)
option_little_size = (30, 60)
option_text_pos = (0, 20)


# TODO I need somehow set level option, and get when its clicked. So I should change this:
class Option(sprite.Sprite):
    def __init__(self, caption="", place=(0, 0), text_place=(0, 0), s=option_size):
        sprite.Sprite.__init__(self, caption, place, s)
        self.text_place = text_place
        self.flick = False
        self.set_font(font.heavy)
        self.update()

    def update(self):
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        if self.flick:
            surf.fill(sec_color)
        text = self.font.render(self.name, 2, (0, 0, 0))
        surf.blit(text, self.text_place)
        self.image = surf


class Menu(surface.Surface):
    def __init__(self, pos=position, s=size, c=color):
        surface.Surface.__init__(self, pos, s, c)
        self.was_hover = None
        self.active = True
        self.init()

    def init(self):
        """
        Init buttons
        :return:
        """
        cont_opt = Option("Continue", (0, 0), (25, option_text_pos[1]))
        next_opt = Option("<", (0, option_size[1]), (0, option_text_pos[1]), option_little_size)
        prev_opt = Option(">", (option_size[0] - option_little_size[0], option_size[1]),
                          (option_little_size[0] - 10, option_text_pos[1]),
                          option_little_size)
        lvl_opt = Option("first", (option_little_size[0], option_size[1]), (20, option_text_pos[1]),
                         (option_size[0] - 2 * option_little_size[0], option_size[1]))
        sound_opt = Option("Sound", (0, option_size[1] * 2), (40, option_text_pos[1]))
        exit_opt = Option("Exit", (0, option_size[1] * 3), (50, option_text_pos[1]))

        self.group.add(cont_opt)
        self.group.add(lvl_opt)
        self.group.add(next_opt)
        self.group.add(prev_opt)
        self.group.add(sound_opt)
        self.group.add(exit_opt)

    def make(self):
        # For hovered elements
        if self.was_hover is not None:
            for i in self.was_hover:
                i.flick = False
                i.update()
        if self.hover is not None:
            for i in self.hover:
                i.flick = True
                i.update()
            self.was_hover = self.hover
