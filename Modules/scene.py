import pygame

import varibles
from robot import Robot

position = (0, 0)
size = (0.75 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = [14, 14, 14]


# ['name', (0, 0)]
# 12x9 by 50

class Scene(pygame.Surface):
    def __init__(self, level, s=size, pos=position):
        pygame.Surface.__init__(self, s)
        self.position = pos
        self.robot = Robot()
        self.level = level
        self.init()
        self.update()

    def update(self):
        self.robot.update()

        tmp = pygame.sprite.Group()
        tmp.add(self.robot)
        tmp.draw(self)

    def init(self):
        print("fix")
