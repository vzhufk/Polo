# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 14.01.2017
from pygame.rect import Rect

import Source.font as font
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

class Robot(pygame.sprite.Sprite):
    def __init__(self, n=name, i_n=image_name, placement=(50, 50)):
        pygame.sprite.Sprite.__init__(self)
        self.name = n
        self.image, self.rect = image(location + i_n + expansion, -1)
        self.original = self.image
        self.rect = Rect(placement[0], placement[1], self.rect[0] + self.rect[2],
                         self.rect[1] + self.rect[3])
        self.fx = float(self.rect.x)
        self.fy = float(self.rect.y)
        self.font = font.medium
        self.direction = 2
        self.update()

    def turn_left(self):
        self.direction -= 1
        self.direction += 4
        self.direction %= 4

    def turn_right(self):
        self.direction += 1
        self.direction %= 4

    # -1 <= percent <= 1
    def move(self, percent):
        if self.direction % 2 == 0:
            self.fy += (1 if self.direction == 2 else -1) * height * percent
            self.rect.y = int(self.fy)
        else:
            self.fx += (1 if self.direction == 1 else -1) * width * percent
            self.rect.x = int(self.fx)

    def update(self):
        self.image = pygame.transform.rotate(self.original, self.direction * -90)

    def place(self, cell):
        self.rect.x = cell[0] * width
        self.rect.y = cell[1] * height
        self.fx = self.rect.x
        self.fy = self.rect.y

    def direct(self, direction):
        self.direction = direction
        self.update()

    def collision(self, position):
        # CORRECTION
        position = (position[0], position[1])
        return self.rect.collidepoint(position)

    def collide_any(self, group):
        for i in group:
            if self.rect.colliderect(i.rect):
                return True, i
        return False, None
