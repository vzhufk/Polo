import pygame
from comtypes.safearray import numpy

import command
import varibles
from program import commands
from robot import Robot
from tile import Tile

position = (0, 0)
size = (0.75 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = [14, 14, 14]

time = 500


# ['name', (0, 0)]
# 12x9 by 50

class Scene(pygame.Surface):
    def __init__(self, s=size, pos=position):
        pygame.Surface.__init__(self, s)
        self.tiles = pygame.sprite.Group()
        self.position = pos
        self.robot = Robot()
        self.program = []
        self.run = False
        self.current = 0
        self.timing = 0
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

    def set_program(self, program):
        # TODO LO & OP conversion
        self.program = program
        self.current = 0
        self.timing = 0

    def get_run(self):
        return self.run

    def event(self, mouse):
        if mouse.get_pressed()[0] and self.robot.collision(numpy.subtract(mouse.get_pos(), self.position)):
            self.run = True

    def move(self, tick):
        self.timing += tick
        if self.timing >= time:
            tick += time - self.timing

        if self.program[self.current] == "forward":
            self.robot.move(tick / time)
        elif self.program[self.current] == "back":
            self.robot.move(-tick / time)
        elif self.program[self.current] == "left":
            self.robot.turn_left()
            self.current += 1
            self.timing %= time
        elif self.program[self.current] == "right":
            self.robot.turn_right()
            self.current += 1
            self.timing %= time

        if self.timing >= time:
            self.current += 1
            self.timing %= time

        # TODO FALL OFF CHECK

        if len(self.program) == self.current:
            self.run = False
            self.current = 0
