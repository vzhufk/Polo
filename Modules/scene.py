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


class Scene(surface.Surface):
    def __init__(self, pos=position, s=size, c=color):
        self.robot = Robot()
        surface.Surface.__init__(self, pos, s, c)
        self.program = []
        # Scene running
        self.launch = False
        self.done = False
        self.success = False
        self.current = -1
        self.timing = 0
        self.update()

    def update(self):
        surface.Surface.update(self)
        self.robot.blit(self)

    def level(self, lvl):
        """
        Loads tile, robot from level
        :param lvl: level class
        :return: ready for game scene
        """
        self.flush()
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
        self.program = program

    def event(self, mouse):
        """
        Events on scene
        :param mouse: pygame.mouse
        :return:
        """
        self.echo = None
        result = []
        if self.is_in(mouse.get_pos()):
            if mouse.get_pressed()[0]:
                if self.robot.collision(self.on_surface(mouse.get_pos())):
                    result.append(self.robot)
                for i in self.group:
                    if i.collision(self.on_surface(mouse.get_pos())):
                        result.append(i)
                self.echo = result

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

    def state(self):
        """
        Checks robot state while running
        :return:
        """
        stand = self.robot.tile_collide(self.group)

        if len(self.program) <= self.current or not stand[0]:
            """If end of program or out of tiles"""
            self.launch = False
            self.done = True
            self.current = -1
            if stand[0]:
                for i in stand[1]:
                    if i.name == "finish":
                        self.success = True

    def start(self):
        self.timing = 0
        self.launch = len(self.program) > 0
        self.current = 0 if self.current < 0 else self.current
        self.done = False
        self.success = False

    def flush(self):
        self.launch = False
        self.done = False
        self.success = False
        self.current = -1
        self.timing = 0

    def step(self, tick):
        """
        Running of scene
        :param tick: time from lst call
        :return: calls robot movement
        """
        self.timing += tick
        if self.timing >= time:
            '''If tick get into 2 different commands in program'''
            self.timing %= time
            self.move(self.program[self.current], tick - self.timing)
            self.current += 1
            if self.current < len(self.program):
                self.move(self.program[self.current], self.timing)
        else:
            self.move(self.program[self.current], tick)

        # Check if we can move more
        self.state()
