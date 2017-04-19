# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 11.02.2017
import pygame

import variables
from Libraries import load
from Modules import sprite
from Modules import surface

position = (25, 0.3 * variables.screen_resolution[1])
size = (variables.screen_resolution[0] - 50, 0.25 * variables.screen_resolution[1])

color = (183, 183, 183)
sec_color = (106, 106, 106)

option_size = (150, 150)
option_little_size = (150, 50)
option_text_pos = (0, 20)
option_location = "Source/Menu/"
option_expansion = ".png"


class OptionImage(sprite.Sprite):
    def __init__(self, name="option", place=(0, 0), s=option_size, image_place=(25, 25), switch=False):
        sprite.Sprite.__init__(self, name, place, s)
        self.flick = False
        self.switch = switch

        if self.switch:
            self.images = []
            self.load_image(option_location + name + "-off" + option_expansion)
            self.place_image(self.image, image_place)
            self.images.append(self.image)
            self.load_image(option_location + name + "-on" + option_expansion)
            self.place_image(self.image, image_place)
            self.images.append(self.image)
            self.switch_index = 1
        else:
            self.load_image(option_location + name + option_expansion)
            # Place
            self.place_image(self.image, image_place)
        # And save
        self.original = self.image

        self.update()

    def toggle(self):
        """
        Toggle switch option
        :return:
        """
        if self.switch:
            self.switch_index += 1
            self.switch_index %= len(self.images)
            self.original = self.images[self.switch_index]

    def update(self):
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        if self.flick:
            surf.fill(sec_color)
        surf.blit(self.original, (0, 0))
        self.image = surf


class OptionText(sprite.Sprite):
    def __init__(self, name="option", caption="sample text", place=(0, 0), text_place=(0, 0), s=option_size,
                 switch=False):
        sprite.Sprite.__init__(self, name, place, s)
        self.caption = caption
        self.caption_place = text_place
        self.switch = switch
        self.flick = False
        self.set_font(variables.font_heavy)
        self.update()

    def update(self):
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        if self.flick:
            surf.fill(sec_color)
        size = self.font.size(self.caption)
        place = ((self.rect.w - size[0]) / 2, (self.rect.h - size[1]) / 2)
        text = self.font.render(self.caption, 2, (0, 0, 0))
        surf.blit(text, place)
        self.image = surf

    def set_caption(self, new_caption):
        """
        Sets new caption
        :param new_caption: text for option
        :return:
        """
        self.caption = str(new_caption)
        self.update()


class Menu(surface.Surface):
    def __init__(self, pos=position, s=size, level=0, c=color):
        surface.Surface.__init__(self, pos, s, c)
        self.level_group = pygame.sprite.Group()
        self.lang_group = pygame.sprite.Group()
        self.level = level
        self.language = 0
        self.levels = load.get_levels(variables.level_path)
        self.languages = load.get_languages(variables.level_path)
        self.was_hover = None
        self.active = True

        self.level_opt = OptionImage("level", (option_size[0], 0))
        self.prev_level_opt = OptionImage("level_prev", (option_size[0], 100), option_little_size, (50, 0))
        self.next_level_opt = OptionImage("level_next", (option_size[0], 0), option_little_size, (50, 0))
        self.choose_level_opt = OptionText("level_choose", self.levels[self.level],
                                           (option_size[0], option_size[1] / 3), (0, 15), option_little_size)

        self.level_group.add(self.level_opt, self.prev_level_opt, self.next_level_opt, self.choose_level_opt)

        self.lang_opt = OptionImage("lang", (option_size[0] * 3, 0))
        self.prev_lang_opt = OptionImage("lang_prev", (option_size[0] * 3, 100), option_little_size, (50, 0))
        self.next_lang_opt = OptionImage("lang_next", (option_size[0] * 3, 0), option_little_size, (50, 0))
        self.choose_lang_opt = OptionText("lang_choose", self.languages[self.language],
                                          (option_size[0] * 3, option_size[1] / 3), (0, 15),
                                          option_little_size)

        self.lang_group.add(self.lang_opt, self.prev_lang_opt, self.next_lang_opt, self.choose_lang_opt)

        cont_opt = OptionImage("play", (0, 0), )
        sound_opt = OptionImage("sound", (option_size[0] * 2, 0), switch=True)

        exit_opt = OptionImage("exit", (option_size[0] * 4, 0))

        self.group.add(self.level_opt, self.lang_opt)
        self.group.add(cont_opt, sound_opt, exit_opt)

    def event(self, mouse, event):
        surface.Surface.event(self, mouse, event)
        # Fade out when cursor is out of menu
        if not self.is_in(mouse.get_pos()) and self.was_hover is not None:
            self.make()

    def set_level(self, lvl):
        """
        Sets new level
        :param lvl: index of level
        :return: 
        """
        self.level = (lvl + len(self.levels)) % len(self.levels)
        self.choose_level_opt.caption = self.levels[self.level]
        self.choose_level_opt.update()

    def set_language(self, lang):
        """
        Updates lang
        :param lang: 
        :return: 
        """
        self.language = (lang + len(self.languages)) % len(self.languages)
        self.choose_lang_opt.caption = self.languages[self.language]
        self.choose_lang_opt.update()

    def make(self):
        """
        Handles all events
        :return:
        """
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

        # Toggle switches
        if self.echo is not None:
            for i in self.echo:
                if i.switch:
                    i.toggle()

        # Level selector
        if self.hover is not None:
            level_hover = False
            for i in self.hover:
                for j in self.level_group:
                    if i == j:
                        level_hover = True
            if level_hover:
                self.group.add(self.choose_level_opt, self.next_level_opt, self.prev_level_opt)
                self.group.remove(self.level_opt)
            else:
                self.group.remove(self.choose_level_opt, self.next_level_opt, self.prev_level_opt)
                self.group.add(self.level_opt)

        # Lang selector
        if self.hover is not None:
            lang_hover = False
            for i in self.hover:
                for j in self.lang_group:
                    if i == j:
                        lang_hover = True
            if lang_hover:
                self.group.add(self.choose_lang_opt, self.next_lang_opt, self.prev_lang_opt)
                self.group.remove(self.lang_opt)
            else:
                self.group.remove(self.choose_lang_opt, self.next_lang_opt, self.prev_lang_opt)
                self.group.add(self.lang_opt)

                # Level scroll
