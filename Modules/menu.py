# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 11.02.2017
import pygame

import varibles

position = (0.3 * varibles.screen_resolution[0], 0.3 * varibles.screen_resolution[1])
size = (0.4 * varibles.screen_resolution[0], 0.4 * varibles.screen_resolution[1])
color = (183, 183, 183)


class Menu(pygame.Surface):
    def __init__(self, s=size, pos=position):
        pygame.Surface.__init__(self, s)
        self.position = pos
        self.rect = pygame.Rect(pos[0], pos[1], s[0], s[1])
        self.command = ""
        self.group = pygame.sprite.Group()
        #        self.init()
        self.update()

    def update(self):
        self.fill(color)

        # TODO event update
        # TODO option class with text
