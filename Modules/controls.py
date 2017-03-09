import varibles
from Modules import command
from Modules import surface
from Modules.command import Command

position = (0.75 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
size = (0.25 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = (183, 183, 183)
sec_color = (106, 106, 106)


class Controls(surface.Surface):
    def __init__(self, pos=position, s=size):

        self.current_direction = 0
        self.direction = 0
        # Hover
        self.was_hover = None

        self.forward = Command("forward", (command.width / 2, command.height / 2))
        self.back = Command("back", (command.width / 2, command.height / 2 + command.height))

        self.right = Command("right", (command.width / 2 + command.width, command.height / 2))
        self.left = Command("left", (command.width / 2 + command.width, command.height / 2 + command.height))

        self.lo = Command("lo", (command.width / 2 + 2 * command.width, command.height / 2))
        self.op = Command("op", (command.width / 2 + 2 * command.width, command.height / 2 + command.height))

        # Because it calls update
        surface.Surface.__init__(self, pos, s)

        self.group.add(self.left, self.right, self.forward, self.back, self.lo, self.op)

    def update(self):
        surface.Surface.update(self)

    def make(self):
        """
        Decrement clicked command
        :return: echo it to other modules
        """
        # For hovered elements
        if self.was_hover is not None:
            for i in self.was_hover:
                i.hover = False
                i.update()
        if self.hover is not None:
            for i in self.hover:
                i.hover = True
                i.update()
            self.was_hover = self.hover

        result = []
        if self.echo is not None:
            for i in self.echo:
                if i.get_amount() > 0:
                    result.append(i)
                    i.change_amount(-1)
                    # If right click place all number of command
                    if self.mouse.get_pressed()[2]:
                        while i.get_amount() > 0:
                            result.append(i)
                            i.change_amount(-1)
        self.echo = result if len(result) > 0 else None

    def direct(self):
        """
        Directing forward and back commands fro comfortable view
        :return:
        """
        self.forward.direction = self.current_direction
        self.back.direction = self.current_direction
        self.forward.update()
        self.back.update()
        self.update()

    def set_delta_direct(self, delta):
        """
        Sets direction by some delta
        :param delta:
        :return:
        """
        self.current_direction = self.direction + delta
        while self.current_direction < 0:
            self.current_direction += 4
        while self.current_direction > 3:
            self.current_direction -= 4
        self.direct()

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
            if name == str(i):
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
        self.current_direction = self.direction
        self.direct()
