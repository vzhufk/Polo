# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 14.01.2017

import Source.font as font
import sprite
from Libraries.load import *

height = 50
width = 50
size = (50, 50)
name = "polo"
image_name = "polo"
location = "Source/Prop/"
expansion = ".png"


# Direction - clock like
# 0 - top
# 1 - right
# 2 - bot
# 3 - left

class Robot(sprite.Sprite):
    def __init__(self, n=name, i_n=image_name, placement=(50, 50)):
        sprite.Sprite.__init__(self, n, placement)
        self.load_image(i_n)
        self.original = self.image
        self.fx = float(self.rect.x)
        self.fy = float(self.rect.y)
        self.set_font(font.medium)
        self.direction = 2

    def turn_left(self):
        """
        Turns robot left
        :return:
        """
        self.direction -= 1
        self.direction += 4
        self.direction %= 4

    def turn_right(self):
        """
        Turns robot right
        :return:
        """
        self.direction += 1
        self.direction %= 4

    def move(self, percent):
        """
        Moving robot on float value
        :param percent: -1 <= percent <= 1 of one step
        :return:
        """
        if self.direction % 2 == 0:
            self.fy += (1 if self.direction == 2 else -1) * height * percent
            self.rect.y = int(self.fy)
        else:
            self.fx += (1 if self.direction == 1 else -1) * width * percent
            self.rect.x = int(self.fx)

    def update(self):
        """
        Rotate image if needed
        :return:
        """
        self.image = pygame.transform.rotate(self.original, self.direction * -90)

    def place(self, cell):
        """
        Placing robot on cell
        :param cell: (0<=x<=12, 0<=y<=9)
        :return: placed robot
        """
        self.rect.x = cell[0] * width
        self.rect.y = cell[1] * height
        self.fx = self.rect.x
        self.fy = self.rect.y

    def direct(self, direction):
        """
        Turns robot to some direction
        :param direction: 0<=direction<=3
        :return:
        """
        self.direction = direction
        self.update()

