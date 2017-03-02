import Source.font as font
from Libraries.load import *
from sprite import Sprite

height = 50
width = 50
size = (50, 50)
def_location = "Source/"
expansion = ".png"


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
        self.original = self.image
        self.fade = False
        self.countable = countable
        self.direction = 0
        self.amount = 0
        self.update()

    def update(self):
        """
        Update sprite if something was changed
        :return:
        """
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        if self.fade:
            surf.set_alpha(128)
        surf.blit(pygame.transform.rotate(self.original, self.direction * -90), (0, 0))
        if self.countable:
            text = self.font.render(str(self.amount), 2, (0, 0, 0))
            surf.blit(text, (self.rect.width - font.size, 0))
        self.image = surf

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
        return Command(self.name, (self.rect.x, self.rect.y))
