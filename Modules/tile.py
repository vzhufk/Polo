# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 19.01.2017
import pygame
from pygame.rect import Rect

import font
import load


class Tile(pygame.sprite.Sprite):
    def __init__(self, name, placement=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        # COLOR KEY ROLLS
        self.image, self.rect = load.image(name, (0, 0, 0, 255))
        self.original = self.image
        self.rect = Rect(placement[0], placement[1], self.rect[0] + self.rect[2],
                         self.rect[1] + self.rect[3])

    def get_name(self):
        return self.name
