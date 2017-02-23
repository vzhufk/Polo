import pygame

import surface
import varibles
from robot import Robot
from tile import Tile

position = (0, 0)
size = (varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = [14, 14, 14]

time = 500


# ['name', (0, 0)]
# 12x9 by 50

def decode(program):
    """
    Decodes program to simple commands. Decode LO and OP to pure commands:
    LO LEFT BACK OP => LEFT BACK LEFT BACK
    :param program: list of string
    :return:
    """
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


class Scene(surface.Surface):
    def __init__(self, pos=position, s=size, c=color):
        surface.Surface.__init__(self, pos, s, c)
        self.robot = Robot()
        self.program = []
        self.success = False
        self.running = False
        self.current = -1
        self.timing = 0
        self.update()

    def update(self):
        surface.Surface.update(self)
        self.robot.update()

        tmp = pygame.sprite.Group()
        tmp.add(self.robot)
        tmp.draw(self)

    def level(self, lvl):
        """
        Loads tile, robot from level
        :param lvl: level class
        :return: ready for game scene
        """
        for i in lvl.tiles:
            self.group.add(Tile(i.type, i.place))

        self.robot.direct(lvl.direction)
        self.robot.place(lvl.placement)
        self.update()

    def set_program(self, program):
        """
        :param program: list of strings - "Dirty" program
        :return:
        """
        self.program = decode(program)
        self.current = 0
        self.timing = 0

    def get_run(self):
        """
        Shows if scene is running
        :return: bool of running
        """
        return self.running

    def get_success(self):
        """
        If robot on exit
        :return: bool get succeed
        """
        return self.success

    def event(self, mouse):
        """
        Events on scene
        :param mouse: pygame.mouse
        :return:
        """
        if self.is_in(mouse.get_pos()):
            if mouse.get_pressed()[0] and self.robot.collision(self.on_surface(mouse.get_pos())):
                self.running = True

    def move(self, command, tick):
        """
        Moving robot according to program
        :param command: current "line" of program
        :param tick: time passed from last call of this function
        :return: moving effect of robot
        """
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
        """
        Stops program and check success
        :return:
        """
        stand = self.robot.collide_group(self.group)
        if len(self.program) == self.current or not stand[0]:
            self.running = False
            self.success = stand[0] and stand[1].name == "finish"
            self.current = -1
            return True
        else:
            return False

    def run(self, tick):
        """
        Running of scene
        :param tick: time from lst call
        :return: calls robot movement
        """
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
