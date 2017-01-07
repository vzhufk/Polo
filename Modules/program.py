import numpy
import pygame

import varibles
from Modules import command
from Modules.command import Command

position = (0, 0.75 * varibles.screen_resolution[1])
size = (0.75 * varibles.screen_resolution[0], 0.25 * varibles.screen_resolution[1])
color = (128, 32, 64)
commands = 10


class Program(pygame.Surface):
    def __init__(self, s=size, pos=position):
        pygame.Surface.__init__(self, s)
        self.group = pygame.sprite.Group()
        self.program = []
        self.position = pos
        self.page = 0
        self.deleted = ""
        self.init()
        self.update()

    def init(self):
        self.update()

    def update(self):
        self.fill(color)
        self.group_up()
        self.group.draw(self)

    def group_up(self):
        self.group = pygame.sprite.Group()
        place = 0
        for i in range(0, len(self.program)):
            if self.page * commands <= i < (self.page + 1) * commands:
                name = str(self.program[i])
                place += command.width
                tmp = Command(name, command.location + name + command.expansion,
                              (place, command.width))
                tmp.uncountable()
                tmp.update()
                self.group.add(tmp)

    def event(self, mouse):
        self.deleted = ""
        if mouse.get_pressed()[0]:
            for i in self.group.sprites():
                if i.collision(numpy.subtract(mouse.get_pos(), self.position)):
                    index = int((mouse.get_pos()[0] - command.width) / command.width)
                    index += self.page * commands
                    if str(self.program[index]) == i.name:
                        self.deleted = str(self.program[index])
                        self.delete(index)
                    break
        self.update()

    def add(self, name):
        self.program.append(name)
        self.update()

    def delete(self, index):
        self.program.pop(index)

    def get_deleted(self):
        return self.deleted
