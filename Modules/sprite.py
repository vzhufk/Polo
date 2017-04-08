# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 22.02.2017
import copy

from pygame.rect import Rect

from Libraries.load import *

height = 50
width = 50
size = (50, 50)
def_location = "Source/"
expansion = ".png"


class Sprite(pygame.sprite.Sprite):
    def __init__(self, name=None, placement=(0, 0), s=size):
        """
        :param name: Sprite name/type etc.
        :param placement: Point related to some surface
        :param s: sprite size
        """
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = None
        self.font = None
        self.group = pygame.sprite.Group()
        self.group.add(self)
        self.rect = Rect(placement[0], placement[1], s[0], s[1])

    def __str__(self):
        """
        :return: Sprite name
        """
        return self.get_name()

    def load_image(self, image_path, key=-1):
        """
        Loads some image into sprite
        :param image_path: path to image
        :return:
        """
        self.image, rect = image(image_path, key)
        # self.rect.width, self.rect.height = rect.width, rect.height

    def set_font(self, some_font):
        """
        Set some ready font for sprite
        :param some_font: pygame.font
        :return:
        """
        self.font = some_font

    def set_name(self, some_name):
        """
        Change sprite name/type/caption etc.
        :param some_name: name
        :return:
        """
        self.name = some_name

    def set_placement(self, point):
        """
        Sets sprite drawing position related to drawing surface
        :param point: tuple of position
        :return:
        """
        self.rect.x = point[0]
        self.rect.y = point[1]

    def get_name(self):
        """
        :return: Sprite name
        """
        return self.name

    def get_position(self):
        """
        :return: Sprite current position related to drawing surface
        """
        return self.rect.x, self.rect.y

    def place_image(self, im, place):
        """
        Placing image on surface in some place
        :param im: pygame.image
        :param place: tuple (x, y)
        :return:
        """
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surf.blit(im, place)
        self.image = surf

    def collision(self, point):
        """
        Check if sprite rect collides with point
        :param point: tuple
        :return: bool of collision
        """
        return self.rect.collidepoint(point)

    def collide_group(self, group):
        """
        Check collision to some group
        :param group: pygame.sprite.Group
        :return: bool, collided sprites
        """
        result = []
        for i in group:
            if self.rect.colliderect(i.rect):
                result.append(i)
        if len(result) == 0:
            return False, None
        else:
            return True, result

    def copy(self):
        """
        :return: Copy of this sprite
        """
        return copy.copy(self)

    def blit(self, surf):
        """
        Blits sprite into surface
        Extension
        :param surf: pygame.surface
        :return:
        """
        self.group.draw(surf)
