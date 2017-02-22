# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 11.02.2017
import pygame
from comtypes.safearray import numpy

import font
import varibles
from sprite import Sprite

position = (0.4 * varibles.screen_resolution[0], 0.3 * varibles.screen_resolution[1])
size = (0.2 * varibles.screen_resolution[0], 0.4 * varibles.screen_resolution[1])
color = (183, 183, 183)

option_size = (320, 60)
option_text_pos = (0, 20)


class Option(Sprite):
    def __init__(self, caption="", place=(0, 0), s=option_size):
        Sprite.__init__(self, caption, place, option_size)
        self.set_font(font.heavy)
        self.update()

    def update(self):
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        text = self.font.render(self.name, 2, (0, 0, 0))
        surf.blit(text, option_text_pos)
        self.image = surf

    def focus(self):
        print("You are on " + self.caption)
        self.update()


class Menu(pygame.Surface):
    def __init__(self, s=size, pos=position):
        pygame.Surface.__init__(self, s)
        self.position = pos
        self.rect = pygame.Rect(pos[0], pos[1], s[0], s[1])
        self.command = ""
        self.options = pygame.sprite.Group()
        self.init()
        self.update()

    def init(self):
        continue_opt = Option("Continue", (0, 0))
        next_opt = Option("Next", (0, option_size[1]))
        prev_opt = Option("Prev", (0, option_size[1] * 2))
        exit_opt = Option("Exit", (0, option_size[1] * 3))
        self.options.add(continue_opt)
        self.options.add(next_opt)
        self.options.add(prev_opt)
        self.options.add(exit_opt)

    def update(self):
        self.fill(color)
        self.options.draw(self)
        # TODO event update
        # TODO option class with text

    def event(self, mouse):
        if self.rect.collidepoint(mouse.get_pos()):
            for i in self.options.sprites():
                if i.collision(numpy.subtract(mouse.get_pos(), self.position)):
                    i.focus()

        self.update()
