import pygame

import variables
from Libraries.decode import decode
from Modules import command
from Modules import surface
from Modules.command import Command

position = (0, 0.75 * variables.screen_resolution[1])
size = (0.75 * variables.screen_resolution[0], 0.25 * variables.screen_resolution[1])
text_color = (0, 0, 0)
color = (200, 200, 200)
sec_color = (106, 106, 106)
commands = 10


class Program(surface.Surface):
    def __init__(self, pos=position, s=size, c=color):
        # Because this module is soo special. You cant believe it. But it is.
        pygame.Surface.__init__(self, s)
        self.rect = pygame.Rect(pos[0], pos[1], s[0], s[1])
        self.group = pygame.sprite.Group()
        self.color = c
        self.font = variables.font_heavy
        self.echo = None
        # End of special needs
        self.direction = 0

        self.page_prev = Command("prev_page", (0, command.height))
        self.page_next = Command("next_page", (size[0] - command.width, command.height))
        self.listing_counter = None
        self.program = []
        self.page = 0
        self.max_page = 0
        self.delete_array = False

        self.init()
        self.update()

    def init(self):
        """
        Init page listing
        :return:
        """
        self.page_next.uncountable()
        self.page_prev.uncountable()
        self.page_next.update()
        self.page_prev.update()

        self.update()

    def update(self):
        """
        Draw everything
        :return:
        """
        self.group_up()
        self.fill(self.color)
        pygame.draw.rect(self, sec_color, (0, 0, command.width, size[1]))
        pygame.draw.rect(self, sec_color, (size[0] - command.width, 0, size[0], size[1]))
        self.group.draw(self)
        self.listing_update()
        self.blit(self.listing_counter, (size[0] / 2, size[1] - 25))

    def listing_update(self):
        """
        Controls Page Listing
        :return: Change or adds page if needed
        """
        self.max_page = int((len(self.program) - 1) / 10)
        if self.page < 0:
            self.page = 0
        if self.page > self.max_page:
            self.page = self.max_page
        self.listing_counter = self.font.render("" + str(self.page + 1) + "/" + str(self.max_page + 1) + "", 2,
                                                text_color)

    def group_up(self):
        """
        Form values on current page of listing
        :return: self.group with commands and listing controls
        """
        self.group = pygame.sprite.Group()
        self.group.add(self.page_next)
        self.group.add(self.page_prev)

        place = 0
        for i in range(0, len(self.program)):
            if self.page * commands <= i < (self.page + 1) * commands:
                place += command.width
                self.program[i].set_placement((place, command.width))
                self.program[i].update()
                self.group.add(self.program[i])

    def make(self):
        """
        Deletes pressed item or change page
        :return:
        """
        echo = []
        if self.echo is not None:
            for i in self.echo:
                if i == self.page_prev:
                    self.page -= 1
                    self.echo = None
                elif i == self.page_next:
                    self.page += 1
                    self.echo = None
                else:
                    # Delete clicked item
                    echo.append(i)
                    index = 0
                    index += (self.page * commands)
                    index += i.rect.x / i.rect.w
                    self.delete(int(index) - 1)
                    # Right click - delete everything to the end of program
                    if (self.mouse is not None and self.mouse.get_pressed()[2]) or str(i) == "lo":
                        for j in range(0, len(self.program) - int(index) + 1):
                            echo.append(self.program[len(self.program) - 1])
                            self.delete(len(self.program) - 1)
        self.echo = echo

    def add(self, items):
        """
        Adds new command in current program
        :param items: chosen sprites(command)
        :return:
        """
        if items is not None:
            for i in items:
                tmp = i.copy()
                tmp.uncountable()
                self.program.append(tmp)
                # If page full get next
                if len(self.program) % commands == 1:
                    self.page += 1
                self.update()

    def delete(self, index):
        """
        Remove item from program list
        :param index: item index
        :return:
        """
        tmp = self.program[index]
        self.program.pop(index)

        # Turn all in program when turn deleted
        if len(self.program) > 0 and (str(tmp) == "left" or str(tmp) == "right"):
            for i in range(0, len(self.program)):
                if str(self.program[i]) == "forward" or str(self.program[i]) == "back":
                    self.program[i].set_direction(self.direction + self.get_delta_direction(0, i))
                else:
                    self.program[i].set_direction(0)

    def get_program(self, start=0, end=None):
        """
        Gets program
        :return: list of sprites
        """
        if end is None:
            end = len(self.program)
        tmp = []
        for i in self.program[start:end]:
            tmp.append(str(i))

        tmp = decode(tmp)
        return tmp

    def get_delta_direction(self, start=0, end=None):
        """
        Decodes program and returns direction change from the beginning
        """
        if end is None:
            end = len(self.program)

        direction = 0
        for i in self.get_program(start, end):
            if str(i) == "right":
                direction += 1
            elif str(i) == "left":
                direction -= 1
        return direction

    def flush(self):
        """
        Flushing all (do i use it?)
        :return:
        """
        self.program.clear()
        self.update()
