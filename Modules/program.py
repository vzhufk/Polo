import numpy
import pygame

import font
import varibles
from Modules import command
from Modules.command import Command

position = (0, 0.75 * varibles.screen_resolution[1])
size = (0.75 * varibles.screen_resolution[0], 0.25 * varibles.screen_resolution[1])
text_color = (0, 0, 0)
color = (200, 200, 200)
sec_color = (106, 106, 106)
commands = 10


class Program(pygame.Surface):
    def __init__(self, s=size, pos=position):
        pygame.Surface.__init__(self, s)
        self.page_prev = Command("prev_page", command.location + "prev_page" + command.expansion, (0, command.height))
        self.page_next = Command("next_page", command.location + "next_page" + command.expansion,
                                 (size[0] - command.width, command.height))
        self.font = font.heavy
        self.group = pygame.sprite.Group()
        self.listing = pygame.sprite.Group()
        self.listing_counter = self.font.render("1/0", 2, text_color)
        self.program = []
        self.position = pos
        self.rect = pygame.Rect(pos[0], pos[1], s[0], s[1])
        self.page = 0
        self.max_page = 0
        self.deleted = ""
        self.init()

    def init(self):
        self.page_next.uncountable()
        self.page_prev.uncountable()
        self.page_next.update()
        self.page_prev.update()

        self.update()

    def update(self):
        self.fill(color)
        pygame.draw.rect(self, sec_color, (0, 0, command.width, size[1]))
        pygame.draw.rect(self, sec_color, (size[0] - command.width, 0, size[0], size[1]))

        self.listing_update()
        self.listing.draw(self)
        self.blit(self.listing_counter, (size[0]/2, size[1]-25))

        self.group_up()
        self.group.draw(self)

    def listing_update(self):
        self.max_page = int((len(self.program)-1) / 10)
        if self.page < 0:
            self.page = 0
        if self.page > self.max_page:
            self.page = self.max_page

        if self.page == 0:
            self.page_prev.fade_out()
        if 0 < self.page:
            self.page_prev.fade_in()
        if self.page < self.max_page:
            self.page_next.fade_in()
        if self.page == self.max_page:
            self.page_next.fade_out()

        self.listing = pygame.sprite.Group()
        self.listing.add(self.page_next)
        self.listing.add(self.page_prev)

        self.listing_counter = self.font.render("" + str(self.page + 1) + "/" + str(self.max_page + 1) + "", 2,
                                                text_color)

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
        if self.rect.collidepoint(mouse.get_pos()):
            if mouse.get_pressed()[0]:
                # Press on command
                for i in self.group.sprites():
                    if i.collision(numpy.subtract(mouse.get_pos(), self.position)):
                        index = int((mouse.get_pos()[0] - command.width) / command.width)
                        index += self.page * commands
                        if str(self.program[index]) == i.name:
                            self.deleted = str(self.program[index])
                            self.delete(index)
                        break
                # Press on listing
                if self.page_next.collision(numpy.subtract(mouse.get_pos(), self.position)):
                    self.page += 1
                if self.page_prev.collision(numpy.subtract(mouse.get_pos(), self.position)):
                    self.page -= 1

            self.update()

    def add(self, name):
        self.program.append(name)
        self.update()

    def delete(self, index):
        self.program.pop(index)

    def get_deleted(self):
        return self.deleted

    def get_program(self):
        return self.program.copy()

    def flush(self):
        self.program.clear()
        self.update()
