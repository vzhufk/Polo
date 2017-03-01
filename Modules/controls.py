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
        """
        Initialize all available commands
        :return:
        """
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
        """
        Decrement clicked command
        :return: echo it to other modules
        """
        result = None
        if self.echo is not None:
            for i in self.echo:
                if i.get_amount() > 0:
                    result = i
                    i.change_amount(-1)
        self.echo = result

    def add(self, item):
        """
        Adds amount to some command
        :param item: sprite with name of addable command
        :return:
        """
        for i in self.group:
            for j in item:
                if j.name == i.name:
                    i.change_amount(1)
        self.update()

    def set(self, name, amount):
        """
        Set amount for command
        :param name: name of command
        :param amount: amount
        :return:
        """
        for i in self.group:
            if name == i.name:
                i.set_amount(int(amount))
        self.update()

    def level(self, lvl):
        """
        Loads commands from level class
        :param lvl: level class
        :return:
        """
        for i in lvl.moves.keys():
            self.set(i, lvl.moves[i])
