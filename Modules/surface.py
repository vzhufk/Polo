# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 22.02.2017

import pygame

import varibles

position = (0.75 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
size = (0.25 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = (183, 183, 183)
sec_color = (106, 106, 106)


class Surface(pygame.Surface):
    def __init__(self, pos=position, s=size, c=color, font=None):
        pygame.Surface.__init__(self, s)
        self.rect = pygame.Rect(pos[0], pos[1], s[0], s[1])
        self.group = pygame.sprite.Group()
        self.color = c
        self.font = font
        self.mouse = None
        self.hover = None
        self.echo = None
        self.update()

    def update(self):
        if self.color is not None:
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
        return point[0] - self.rect.x, point[1] - self.rect.y

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

    def event(self, mouse, event):
        """
        Mouse press event. Return sprites which was clicked
        :param mouse: pygame.mouse
        :return: list of clicked sprites into self.echo
        """
        self.echo = None
        self.hover = None
        if self.is_in(mouse.get_pos()):
            self.hover = (self.collide_all(mouse.get_pos()))
            self.mouse = mouse
            if event.type == pygame.MOUSEBUTTONUP:
                self.echo = self.hover
            self.make()

    def make(self):
        pass

    def set_position(self, pos):
        """
        Sets new windows position
        :param pos:
        :return:
        """
        self.rect.x = pos[0]
        self.rect.y = pos[1]

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
        self.update()
        return self.echo

    def echo_out(self):
        """
        Clears echo after get
        :return:
        """
        self.echo = None

    def flush(self):
        """
        Flush to start state
        :return:
        """
        self.group = pygame.sprite.Group()
        self.hover = None
        self.echo = None
