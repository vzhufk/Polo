import pygame

import varibles
from robot import Robot
from tile import Tile

position = (0, 0)
size = (0.75 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = [14, 14, 14]


# ['name', (0, 0)]
# 12x9 by 50

class Scene(pygame.Surface):
    def __init__(self, s=size, pos=position):
        pygame.Surface.__init__(self, s)
        self.tiles = pygame.sprite.Group()
        self.position = pos
        self.robot = Robot()
        self.init()
        self.update()

    def update(self):
        self.tiles.draw(self)

        self.robot.update()
        tmp = pygame.sprite.Group()
        tmp.add(self.robot)
        tmp.draw(self)

    def init(self, ):
        print("fix")

    def level(self, lvl):
        for i in lvl.tiles:
            self.tiles.add(Tile(i.location, i.place))
        self.update()
