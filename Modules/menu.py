# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 11.02.2017
import pygame

import font
import load
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

class Option(sprite.Sprite):
    def __init__(self, name="option", caption="sample text", place=(0, 0), text_place=(0, 0), s=option_size):
        sprite.Sprite.__init__(self, name, place, s)
        self.caption = caption
        self.caption_place = text_place
        self.flick = False
        self.set_font(font.heavy)
        self.update()

    def update(self):
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        if self.flick:
            surf.fill(sec_color)
        text = self.font.render(self.caption, 2, (0, 0, 0))
        surf.blit(text, self.caption_place)
        self.image = surf

    def set_caption(self, new_caption):
        self.caption = new_caption


class Menu(surface.Surface):
    def __init__(self, pos=position, s=size, level=0, c=color):
        surface.Surface.__init__(self, pos, s, c)
        self.current_level = level
        self.level_count = len(load.get_levels(varibles.level_path))
        self.was_hover = None
        self.active = True
        self.init()

    def init(self):
        """
        Init buttons
        :return:
        """
        cont_opt = Option("continue", "Continue", (0, 0), (25, option_text_pos[1]))
        next_opt = Option("prev", "<", (0, option_size[1]), (0, option_text_pos[1]), option_little_size)
        prev_opt = Option("next", ">", (option_size[0] - option_little_size[0], option_size[1]),
                          (option_little_size[0] - 10, option_text_pos[1]), option_little_size)
        # Because I need it to change thought
        self.level_opt = Option("level", load.get_levels()[self.current_level], (option_little_size[0], option_size[1]),
                                (20, option_text_pos[1]), (option_size[0] - 2 * option_little_size[0], option_size[1]))
        sound_opt = Option("sound", "Sound", (0, option_size[1] * 2), (40, option_text_pos[1]))
        exit_opt = Option("exit", "Exit", (0, option_size[1] * 3), (50, option_text_pos[1]))

        self.group.add(cont_opt)
        self.group.add(self.level_opt)
        self.group.add(next_opt)
        self.group.add(prev_opt)
        self.group.add(sound_opt)
        self.group.add(exit_opt)

    def update_level(self):
        self.level_opt.set_caption(load.get_levels()[self.current_level])

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

        if self.echo is not None:
            for i in self.echo:
                if i.name == "prev":
                    self.current_level -= 1 if self.current_level > 0 else 0
                    self.update_level()
                elif i.name == "next":
                    self.current_level += 1 if self.current_level < self.level_count - 1 else 0
                    self.update_level()
