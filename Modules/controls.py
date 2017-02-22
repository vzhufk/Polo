import numpy

import surface

import varibles
from Modules import command
from Modules.command import Command

position = (0.75 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
size = (0.25 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = (183, 183, 183)
sec_color = (106, 106, 106)


class Controls(surface.Surface):
    def __init__(self, pos=position, s=size):
        surface.Surface.__init__(self, pos, s)
        self.init_commands()

    def init_commands(self):
        front = Command("forward", (command.width / 2, command.height / 2))
        back = Command("back", (command.width / 2, command.height / 2 + command.height))

        right = Command("right", (command.width / 2 + command.width, command.height / 2))
        left = Command("left", (command.width / 2 + command.width, command.height / 2 + command.height))

        lo = Command("lo", (command.width / 2 + 2 * command.width, command.height / 2))
        op = Command("op", (command.width / 2 + 2 * command.width, command.height / 2 + command.height))

        self.group.add(left)
        self.group.add(right)
        self.group.add(front)
        self.group.add(back)
        self.group.add(lo)
        self.group.add(op)

    def make(self):
        result = None
        for i in self.echo:
            if i.get_amount() > 0:
                result = i
                i.change_amount(-1)
        self.echo = result

    def add(self, item):
        for i in self.group:
            for j in item:
                if j.name == i.name:
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
