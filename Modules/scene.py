import pygame
from comtypes.safearray import numpy

import varibles
from robot import Robot
from tile import Tile

position = (0, 0)
size = (0.75 * varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = [14, 14, 14]

time = 500


# ['name', (0, 0)]
# 12x9 by 50

def decode(program):
    result = []
    i = 0
    while i < len(program):
        if program[i] == "lo":
            lo = 1
            j = i + 1
            while lo > 0:
                if j == len(program):
                    program.append("op")

                if program[j] == "lo":
                    lo += 1
                elif program[j] == "op":
                    lo -= 1

                j += 1 if lo > 0 else 0
            if i + 1 == j - 1:
                tmp = [program[i + 1]]
            else:
                tmp = program[i + 1:j]
            del program[j]
            del program[i]
            program[i:i] = tmp
            i -= 1
        elif program[i] == "op":
            program[0:0] = ["lo"]
            i = 0
            result = []
        else:
            result.append(program[i])
        i += 1
    return result


# TODO Rebase

class Scene(pygame.Surface):
    def __init__(self, s=size, pos=position):
        pygame.Surface.__init__(self, s)
        self.tiles = pygame.sprite.Group()
        self.rect = pygame.Rect(pos[0], pos[1], s[0], s[1])
        self.position = pos
        self.robot = Robot()
        self.program = []
        self.success = False
        self.running = False
        self.current = -1
        self.timing = 0
        self.update()

    def update(self):
        self.fill((0, 0, 0))
        self.tiles.draw(self)

        tmp = pygame.sprite.Group()
        tmp.add(self.robot)
        tmp.draw(self)

    def level(self, lvl):
        for i in lvl.tiles:
            self.tiles.add(Tile(i.type, i.place))

        self.robot.direct(lvl.direction)
        self.robot.place(lvl.placement)
        self.robot.update()
        self.update()

    def set_program(self, program):
        self.program = decode(program)
        self.current = 0
        self.timing = 0

    def get_run(self):
        return self.running

    def get_success(self):
        return self.success

    def event(self, mouse):
        if self.rect.collidepoint(mouse.get_pos()):
            if mouse.get_pressed()[0] and self.robot.collision(numpy.subtract(mouse.get_pos(), self.position)):
                self.running = True

    def move(self, command, tick):
        if command == "forward":
            self.robot.move(tick / time)
        elif command == "back":
            self.robot.move(-tick / time)
        elif command == "left":
            self.robot.turn_left()
            self.current += 1
            self.timing %= time
            self.robot.update()
        elif command == "right":
            self.robot.turn_right()
            self.current += 1
            self.timing %= time
            self.robot.update()

    def stop(self):
        stand = self.robot.collide_any(self.tiles)
        if len(self.program) == self.current or not stand[0]:
            self.running = False
            self.success = stand[0] and stand[1].name == "finish"
            self.current = -1
            return True
        else:
            return False

    def run(self, tick):
        self.current = 0 if self.current < 0 else self.current
        if not self.stop():
            self.timing += tick

            if self.timing >= time:
                self.timing %= time
                self.move(self.program[self.current], tick - self.timing)
                self.current += 1
                if self.current < len(self.program):
                    self.move(self.program[self.current], self.timing)
            else:
                self.move(self.program[self.current], tick)
