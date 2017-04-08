import pygame

import varibles
from Libraries import load
from Modules import surface
from Modules.robot import Robot
from Modules.tile import Tile

position = (0, 0)
size = (varibles.screen_resolution[0], 0.75 * varibles.screen_resolution[1])
color = [14, 14, 14]

speed_up = 5
time = 1000

background_music = "background.wav"
background_music_volume = 0.15
def_location = "Source/"


# ['name', (0, 0)]
# 12x9 by 50


class Scene(surface.Surface):
    def __init__(self, pos=position, s=size, c=color):
        self.robot = Robot()
        surface.Surface.__init__(self, pos, s, c)
        # Background music
        self.background_music = load.sound(def_location + background_music)
        self.background_music.play(-1)
        self.background_music.set_volume(background_music_volume)
        # Scene program from engine
        self.program = []
        # Scene running
        self.launch = False
        # Program running finished
        self.done = False
        # Program succeeded
        self.success = False
        # Death on scene (robot death)
        self.death = False
        # Current command in program
        self.current = -1
        # Current scene time
        self.timing = 0
        # Speed up option
        self.speed_up = False
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

    def event(self, mouse, event):
        """
        Events on scene
        :param mouse: pygame.mouse
        :return:
        """
        self.echo = None
        result = []
        if self.is_in(mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONUP:
                if self.robot.collision(self.on_surface(mouse.get_pos())):
                    result.append(self.robot)
                for i in self.group:
                    if i.collision(self.on_surface(mouse.get_pos())):
                        result.append(i)
                self.echo = result

    def action(self, command, tick):
        """
        Moving robot according to program
        :param command: current "line" of program
        :param tick: time passed from last call of this function
        :return: moving effect of robot
        """
        if command == "die":
            self.robot.death(tick / time)
        elif command == "forward":
            self.robot.move(tick / time)
        elif command == "back":
            self.robot.move(-tick / time)
        elif command == "left":
            self.robot.turn(-tick / time)
            self.robot.update()
        elif command == "right":
            self.robot.turn(tick / time)
            self.robot.update()

    def state(self):
        """
        Checks robot state while running
        :return:
        """
        # Sprites on which Polo is standing
        stand = self.robot.tile_collide(self.group)
        # Means end of road, and reload
        if len(self.program) <= self.current or (self.death and not self.robot.dying()):
            """If end of program or out of tiles"""
            self.launch = False
            self.done = True
            self.current = -1
            if stand[0]:
                for i in stand[1]:
                    if i.name == "finish":
                        self.success = True
        # Means death (if robot out of tiles)
        if not self.death and not stand[0]:
            self.robot.death_sound.play()
        self.death = not stand[0]

    def start(self):
        """
        Setups start of scene
        :return:
        """
        self.done = False
        self.death = False
        self.success = False
        self.speed_up = False
        self.timing = 0
        self.launch = len(self.program) > 0
        self.current = 0 if self.current < 0 else self.current

    def flush(self):
        """
        Scene flush
        :return:
        """
        surface.Surface.flush(self)
        self.robot.flush()
        self.start()
        self.launch = False
        self.speed_up = False
        self.current = -1

    def step(self, tick):
        """
        Running of scene
        :param tick: time from lst call
        :return: calls robot movement
        """
        # If death called from state()
        if self.death:
            # Perform die action
            self.action("die", tick * speed_up * speed_up)
            # Call end of program
        else:
            if self.speed_up:
                tick *= speed_up
            self.timing += tick
            if self.timing >= time:
                '''If tick get into 2 different commands in program'''
                self.timing %= time
                self.action(self.program[self.current], tick - self.timing)
                self.current += 1
                if self.current < len(self.program):
                    self.action(self.program[self.current], self.timing)
            else:
                self.action(self.program[self.current], tick)

        # Check if we can move more
        self.state()
