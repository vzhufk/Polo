# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 14.01.2017

import Source.font as font
from Libraries import load
from Libraries.load import *
from Modules import sprite

height = 50
width = 50
size = (50, 50)
name = "polo"
death = "long_explosion"
def_location = "Source/Prop/"
expansion = ".png"

sound_explosion = "bam-motherfucker.wav"
sound_volume = 0.4
# Direction - clock like
# 0 - top
# 1 - right
# 2 - bot
# 3 - left


# TODO Think about rotate and scale down death :)
class Robot(sprite.Sprite):
    def __init__(self, n=name, i_n=None, placement=(50, 50)):
        sprite.Sprite.__init__(self, n, placement)
        i_n = i_n if i_n is not None else def_location + n + expansion
        self.load_image(i_n)
        self.dead = False
        self.death_sprites = load.load_sliced_sprite(def_location + death + expansion, width, height)
        self.death_sprite_current = 0.0
        self.death_sound = load.sound(def_location + sound_explosion)
        self.death_sound.set_volume(sound_volume)
        self.original = self.image
        self.fx = float(self.rect.x)
        self.fy = float(self.rect.y)
        self.set_font(font.medium)
        self.direction = 2

    def flush(self):
        self.dead = False
        self.death_sprite_current = 0.0
        self.update()

    def turn(self, value):
        """
        Turns robot on degree
        :param value: float 0<=float<=3 1 = 90 ; value = 2 == Pi
        :return:
        """
        self.direction = float(self.direction) + float(value)
        self.turn_normalize()

    def turn_normalize(self):
        if self.direction < 0:
            self.direction += 4
        elif self.direction >= 4:
            self.direction -= 4

    def turn_left(self):
        """
        Turns robot left
        :return:
        """
        self.direction -= 1
        self.turn_normalize()

    def turn_right(self):
        """
        Turns robot right
        :return:
        """
        self.direction += 1
        self.turn_normalize()

    def move(self, percent):
        """
        Moving robot on float value
        :param percent: -1 <= percent <= 1 of one step
        :return:
        """

        self.direction = int(round(self.direction))
        if int(round(self.direction)) % 2 == 0:
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
        if not self.dead:
            self.image = pygame.transform.rotate(self.original, self.direction * -90)
            # To rotate around center
            self.rect = self.image.get_rect(center=self.rect.center)
        sprite.Sprite.update(self)

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

    def tile_collide(self, group):
        """
        Checks robot collision to tile
        Actually its just collision to the center of sprite
        :param group:
        :return:
        """
        result = []
        point = (self.rect[0] + self.rect[2] / 2, self.rect[1] + self.rect[3] / 2)
        for i in group:
            if i.collision(point):
                result.append(i)

        if len(result) == 0:
            return False, None
        else:
            return True, result

    def death(self, percent=1.0):
        """
        Performs death of robot
        :param percent: 0<=percent<=1 1 equals one frame from death animation
        :return:
        """
        self.death_sprite_current += percent
        if self.dying():
            self.image = self.death_sprites[int(self.death_sprite_current)]

    def dying(self):
        """
        Shows if robot is still dying, or already dead.
        :return:
        """
        return len(self.death_sprites) > self.death_sprite_current >= 0
