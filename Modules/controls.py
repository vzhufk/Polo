import numpy
import pygame

import varibles
from Modules import command
from Modules.command import Command

position = (0.75 * varibles.screen_resolution[0], 0.25 * varibles.screen_resolution[1])
size = (0.25 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = (63, 81, 181)


class Controls(pygame.Surface):
    def __init__(self, s=size, pos=position):
        pygame.Surface.__init__(self, s)
        self.position = pos
        self.command = ""
        self.group = pygame.sprite.Group()
        self.init()
        self.update()

    def init(self):

        right = Command("right", command.location + "right" + command.expansion, command.size)
        left = Command("left", command.location + "left" + command.expansion, (command.width * 2, command.height))
        front = Command("forward", command.location + "forward" + command.expansion,
                        (command.width, command.height * 2))
        back = Command("back", command.location + "back" + command.expansion, (command.width * 2, command.height * 2))
        lo = Command("lo", command.location + "lo" + command.expansion, (command.width, command.height * 3))
        op = Command("op", command.location + "op" + command.expansion, (command.width * 2, command.height * 3))

        self.group.add(left)
        self.group.add(right)
        self.group.add(front)
        self.group.add(back)
        self.group.add(lo)
        self.group.add(op)

    def update(self):
        self.fill(color)
        self.group.draw(self)

    def event(self, mouse):
        self.command = ""
        if mouse.get_pressed()[0]:
            for i in self.group.sprites():
                if i.collision(numpy.subtract(mouse.get_pos(), self.position)):
                    if i.get_amount() > 0:
                        self.command = i.name
                    i.change_amount(-1)
        self.update()

    def get_command(self):
        return self.command

    def add(self, name):
        for i in self.group:
            if name == i.name:
                i.change_amount(1)
        self.update()
