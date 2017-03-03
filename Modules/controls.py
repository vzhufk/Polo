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

        self.direction = 0

        self.forward = Command("forward", (command.width / 2, command.height / 2))
        self.back = Command("back", (command.width / 2, command.height / 2 + command.height))

        self.right = Command("right", (command.width / 2 + command.width, command.height / 2))
        self.left = Command("left", (command.width / 2 + command.width, command.height / 2 + command.height))

        self.lo = Command("lo", (command.width / 2 + 2 * command.width, command.height / 2))
        self.op = Command("op", (command.width / 2 + 2 * command.width, command.height / 2 + command.height))

        # Because it calls update
        surface.Surface.__init__(self, pos, s)

        self.group.add(self.left)
        self.group.add(self.right)
        self.group.add(self.forward)
        self.group.add(self.back)
        self.group.add(self.lo)
        self.group.add(self.op)

    def update(self):
        surface.Surface.update(self)

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
        # To turn direction
        if self.echo is not None:
            if i.name == "left":
                self.direction -= 1 if self.direction > 0 else -3
                self.direct()
            elif i.name == "right":
                self.direction += 1 if self.direction < 3 else -3
                self.direct()

    def direct(self):
        self.forward.direction = self.direction
        self.back.direction = self.direction
        self.forward.update()
        self.back.update()

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
                    # For direction
                    if j.name == "right":
                        self.direction -= 1 if self.direction > 0 else -3
                        self.direct()
                    elif j.name == "left":
                        self.direction += 1 if self.direction < 3 else -3
                        self.direct()
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
        self.direction = lvl.direction
        self.direct()
