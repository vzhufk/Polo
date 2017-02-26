import pygame

import font
import surface
import varibles
from Modules import command
from Modules.command import Command
from decode import decode

position = (0, 0.75 * varibles.screen_resolution[1])
size = (0.75 * varibles.screen_resolution[0], 0.25 * varibles.screen_resolution[1])
text_color = (0, 0, 0)
color = (200, 200, 200)
sec_color = (106, 106, 106)
commands = 10


class Program(surface.Surface):
    def __init__(self, pos=position, s=size, c=color):
        surface.Surface.__init__(self, pos, s, c)
        self.page_prev = Command("prev_page", (0, command.height))
        self.page_next = Command("next_page", (size[0] - command.width, command.height))
        self.set_font(font.heavy)
        self.listing_counter = None
        self.program = []
        self.page = 0
        self.max_page = 0
        self.init()

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
        ''' Temporary removed
        if self.page == 0:
            self.page_prev.fade_out()
        if 0 < self.page:
            self.page_prev.fade_in()
        if self.page < self.max_page:
            self.page_next.fade_in()
        if self.page == self.max_page:
            self.page_next.fade_out()
        '''
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
                tmp = self.program[i].copy()
                tmp.set_placement((place, command.width))
                tmp.uncountable()
                tmp.update()
                self.group.add(tmp)

    def make(self):
        """
        Deletes pressed item or change page
        :return:
        """
        echo = []
        for i in self.echo:
            if i.name == "prev_page":
                self.page -= 1
                self.echo = None
            elif i.name == "next_page":
                self.page += 1
                self.echo = None
            else:
                echo.append(i)
                # because we have page turn command which adds extra 1
                index = -1
                index += (self.page * commands)
                index += i.rect.x / i.rect.w
                self.delete(int(index) - 1)
        self.echo = echo

    def add(self, item):
        """
        Adds new command in current program
        :param item: chosen sprite(command)
        :return:
        """
        self.program.append(item)
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
        self.program.pop(index)

    def get_program(self):
        """
        Gets program
        :return: list of sprites
        """
        # TODO Should I modify it to list of strings???
        # TODO Just for now
        tmp = []
        for i in self.program:
            tmp.append(str(i))

        tmp = decode(tmp)
        return tmp

    def flush(self):
        """
        Flushing all (do i use it?)
        :return:
        """
        self.program.clear()
        self.update()
