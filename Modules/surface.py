# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 22.02.2017

import numpy
import pygame

import varibles
from Modules import command
from Modules.command import Command

position = (0.75 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
size = (0.25 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = (183, 183, 183)
sec_color = (106, 106, 106)


class Surface(pygame.Surface):
    def __init__(self, pos=position, s=size, c=color):
        pygame.Surface.__init__(self, s)
        self.rect = pygame.Rect(pos[0], pos[1], s[0], s[1])
        self.group = pygame.sprite.Group()
        self.color = c
        self.font = None
        self.echo = None

    def update(self):
        self.fill(self.color)
        self.group.draw(self)

    def is_in(self, point):
        """
        Checks if point is in the surface
        :param point: tuple
        :return: Bool
        """
        return self.rect.collidepoint(point)

    def on_surface(self, point):
        """
        Transpose point from screen related to surface related
        :param point:
        :return:
        """
        return numpy.subtract(point, (self.rect.x, self.rect.y))

    def collide_all(self, point):
        """
        Get collision from point to all sprites
        :param point: tuple
        :return: list of collided sprites
        """
        result = list()
        point = self.on_surface(point)
        for i in self.group.sprites():
            if i.collision(point):
                result.append(i)
        return result

    def event(self, mouse):
        """
        Mouse press event. Return sprites which was clicked
        :param mouse: pygame.mouse
        :return: list of clicked sprites into self.echo
        """
        self.echo = None
        if mouse.get_pressed()[0] and self.is_in(mouse.get_pos()):
            self.set_echo(self.collide_all(mouse.get_pos()))
            self.make()
        self.update()

    def make(self):
        print(self.echo)

    def set_echo(self, value):
        """
        Set echos param
        :param value: any
        :return:
        """
        self.echo = value

    def set_font(self, some_font):
        """
        Sets font for surf
        :param some_font: pygame.font
        :return:
        """
        self.font = some_font

    def get_echo(self):
        """
        Gets echo
        :return: echo any
        """
        return self.echo
