import Source.font as font
from Libraries.load import *
from Modules.sprite import Sprite

height = 50
width = 50
size = (50, 50)
def_location = "Source/"
expansion = ".png"

color = (200, 200, 200)
sec_color = (106, 106, 106)


class Command(Sprite):
    def __init__(self, name, placement=(0, 0), image_path=None, s=size, countable=True):
        """
        :param name: Command name
        :param placement: Placement related to surface
        :param image_path: Directory of image that is used for command
        :param s: size of command sprite
        """
        Sprite.__init__(self, name, placement, s)
        image_path = image_path if image_path is not None else def_location + name + expansion
        self.load_image(image_path)
        self.set_font(font.medium)
        self.big_font = font.shaded
        # Original start ima
        self.original = self.image
        # Counting on command
        self.countable = countable
        # Direction of command
        self.direction = 0
        # Fade out
        self.fade = False
        # Hover
        self.hover = False
        # Available amount of command
        self.amount = 0
        self.update()

    def update(self):
        """
        Update sprite if something was changed
        :return:
        """
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surf.blit(pygame.transform.rotate(self.original, self.direction * -90), (0, 0))
        if self.countable:
            if self.hover:
                text = self.big_font.render(str(self.amount), 2, (0, 0, 0))
                text_size = self.big_font.size(str(self.amount))
                surf.blit(text, ((self.rect.width - text_size[0]) / 2, (self.rect.height - text_size[1]) / 2))
            else:
                text = self.font.render(str(self.amount), 2, (0, 0, 0))
                text_size = self.font.size(str(self.amount))
                surf.blit(text, (self.rect.width - text_size[0], 0))
        self.image = surf

    def delta_direction(self, delta):
        """Changes direction by delta"""
        self.direction += delta
        while self.direction < 0:
            self.direction += 4
        while self.direction > 3:
            self.direction -= 4

    def set_direction(self, direction):
        """
        Set direction
        :param direction:
        :return:
        """
        self.direction = int(direction)
        while self.direction < 0:
            self.direction += 4
        while self.direction > 3:
            self.direction -= 4

    def set_amount(self, amount):
        """
        :param amount: Current available amount of this command
        :return: updates sprite with new amount
        """
        self.amount = amount
        self.change_amount(0)
        self.update()

    def change_amount(self, dif):
        """
        :param dif: Change of current available amount of this command
        :return: New current amount, updates sprite, fade it in/out
        """
        self.amount += dif
        if self.amount <= 0:
            self.amount, self.fade = 0, True
        else:
            self.fade = False
        self.update()

    def fade_out(self):
        """
        :return: Makes fade - True, and in update() it have to fade out
        """
        self.fade = True
        self.update()

    def fade_in(self):
        """
        :return: Makes fade - False, and in update() it have to fade in
        """
        self.fade = False
        self.update()

    def get_amount(self):
        """
        :return: Available amount of this command
        """
        return self.amount

    def __int__(self):
        """
        :return: Available amount of this command
        """
        return self.get_amount()

    def uncountable(self):
        """
        :return: Amount of command no longer shows on sprite
        """
        self.countable = False

    def countable(self):
        """
        :return: Amount of command would shows on sprite
        """
        self.countable = True

    def reverse_countable(self):
        """
        :return: Amount show/muck
        """
        self.countable = not self.countable

    def copy(self):
        """
        Try to copy
        :return:
        """
        tmp = Command(self.name, (self.rect.x, self.rect.y))
        tmp.direction = self.direction
        return tmp
