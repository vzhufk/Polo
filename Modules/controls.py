import numpy
import pygame

import varibles
from Modules import command
from Modules.command import Command

position = (0.75 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
size = (0.25 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = (183, 183, 183)
sec_color = (106, 106, 106)

class Controls(pygame.Surface):
    def __init__(self, s=size, pos=position):
        pygame.Surface.__init__(self, s)
        self.position = pos
        self.command = ""
        self.group = pygame.sprite.Group()
        self.init()
        self.update()

    def init(self):

        front = Command("forward", command.location + "forward" + command.expansion,
                        (command.width / 2, command.height / 2))
        back = Command("back", command.location + "back" + command.expansion, (command.width / 2, command.height / 2 +
                                                                               command.height))

        right = Command("right", command.location + "right" + command.expansion, (command.width / 2 + command.width,
                                                                                  command.height / 2))
        left = Command("left", command.location + "left" + command.expansion, (command.width / 2 + command.width,
                                                                               command.height / 2 + command.height))

        lo = Command("lo", command.location + "lo" + command.expansion, (command.width / 2 + 2 * command.width,
                                                                         command.height / 2))
        op = Command("op", command.location + "op" + command.expansion, (command.width / 2 + 2 * command.width,
                                                                         command.height / 2 + command.height))

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

    def set(self, name, amount):
        for i in self.group:
            if name == i.name:
                i.set_amount(amount)
        self.update()

    def level(self, lvl):
        for i in lvl.moves.keys():
            self.set(i, lvl.moves[i])
