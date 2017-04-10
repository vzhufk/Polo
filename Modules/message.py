import pygame

import varibles
from Modules import command
from Modules import sprite
from Modules import surface
from Source import font
from command import Command

position = (0, 0.75 * varibles.screen_resolution[1])
size = (varibles.screen_resolution[0], 0.25 * varibles.screen_resolution[1])
text_color = (0, 0, 0)
color = (200, 200, 200)
sec_color = (106, 106, 106)
text_color = (0, 0, 0)
text_pos = (20, 20)
line_length_limit = 60


class MessageText(sprite.Sprite):
    def __init__(self, text="SAMPLE TEXT", place=(0, 0), s=size, t_p=text_pos):
        sprite.Sprite.__init__(self, text, place, s)
        self.text_pos = t_p
        self.font = font.message_text
        self.text = text
        self.update()

    def update(self):
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        current = text_pos
        text = self.text
        while len(text) > line_length_limit:
            index = text.rfind(" ", 0, line_length_limit)
            index = line_length_limit if index < 0 else index
            line = text[:index]
            text = text[index + 1:]
            text_size = self.font.size(line)
            text_rend = self.font.render(line, 2, text_color)
            surf.blit(text_rend, current)
            current = (current[0], current[1] + text_size[1])
        text_rend = self.font.render(text, 2, text_color)
        surf.blit(text_rend, current)
        self.image = surf


class Message(surface.Surface):
    def __init__(self, pos=position, s=size, c=color):
        pygame.Surface.__init__(self, s)
        self.text = []
        self.page = 0
        self.rect = pygame.Rect(pos[0], pos[1], s[0], s[1])
        self.group = pygame.sprite.Group()
        self.set_position(pos)
        self.color = c
        self.echo = None

        self.page_next = Command("next_page", (size[0] - command.width, command.height))
        self.page_next.uncountable()
        self.page_next.update()

    def update(self):
        """
        Draw everything
        :return:
        """
        self.fill(self.color)
        self.group = pygame.sprite.Group()
        self.group.add(self.page_next)
        if self.page < len(self.text):
            self.group.add(MessageText(self.text[self.page]))
        pygame.draw.rect(self, sec_color, (size[0] - command.width, 0, size[0], size[1]))
        self.group.draw(self)

    def make(self):
        """
        Deletes pressed item or change page
        :return:
        """
        echo = []
        if self.echo is not None:
            for i in self.echo:
                if i == self.page_next:
                    self.page += 1
                    self.update()
                    self.echo = None
                    if self.page >= len(self.text):
                        echo = "end"
        self.echo = echo

    def set_text(self, text):
        """
        Sets text for message
        :param text: list of strings
        :return: 
        """
        self.text = text

    def flush(self):
        """
        Flushing all (do i use it?)
        :return:
        """
        self.page = 0
        self.update()
