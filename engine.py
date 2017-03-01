import os
import sys

import pygame

import varibles
from Modules.controls import Controls
from Modules.program import Program
from level import Level
from menu import Menu
from scene import Scene

FPS = varibles.FPS
window_title = varibles.window_title
screen_resolution = varibles.screen_resolution
screen_mode = varibles.screen_mode

'''
    TODO TOTHINK Can try some double "thread" mode. We have two robots. And commands for them the same, but positions
    are different.
    TOTHINK Coop multilayer Portal2 like. Robots have to meet in custom place.
    TOTHINK TODO SOMETHING WITH LIFE
'''


class Engine:
    def __init__(self):
        pygame.init()
        self.scene_run = False
        self.pause = False
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)
        pygame.display.set_caption(window_title)
        self.display = pygame.display.set_mode(screen_resolution)
        self.clock = pygame.time.Clock()
        self.level = Level("demo")
        self.controls = Controls()
        self.program = Program()
        self.scene = Scene()
        self.menu = Menu()

    def load(self, name):
        self.level = Level(name)
        self.level.load()
        # Pass level to other modules
        self.controls.level(self.level)
        self.scene.level(self.level)

    def reload(self):
        self.scene.level(self.level)

    def blit(self):
        self.display.blit(self.controls, self.controls.rect)
        self.display.blit(self.program, self.program.rect)
        self.display.blit(self.scene, self.scene.rect)

        if self.pause:
            self.display.blit(self.menu, self.menu.rect)
            # TODO Maybe Blur effect in pause

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit()

            if self.pause:
                self.menu.event(pygame.mouse)
            else:
                self.controls.event(pygame.mouse)
                self.program.event(pygame.mouse)
                self.scene.event(pygame.mouse)

                """If was pressed key while robot was moving"""
                """Just reload"""
                # TODO Or speed it up???
                # I can just change time in scene to speed up
                if self.scene.launch and pygame.mouse.get_pressed()[0]:
                    self.reload()

            self.invoker()

    def invoker(self):
        """
        Invokes module calls
        :return:
        """
        """Controls Echos"""
        if self.controls.get_echo() is not None:
            self.program.add(self.controls.get_echo())
            self.controls.echo_out()

        """Program Echos"""
        if self.program.get_echo() is not None:
            self.controls.add(self.program.get_echo())
            self.program.echo_out()

        """Scene Echos"""
        if self.scene.get_echo() is not None:
            self.scene_handler()
            self.scene.echo_out()

        """Menu Echos"""
        if self.menu.get_echo() is not None:
            self.menu_handler()
            self.menu.echo_out()

    def menu_handler(self):
        for i in self.menu.get_echo():
            if str(i) == "Continue":
                self.pause = False
            elif str(i) == "Exit":
                self.exit()

    def scene_handler(self):
        for i in self.scene.echo:
            if i.name == "finish":
                self.pause = True
            elif i.name == "polo":
                self.setup_scene()

    def setup_scene(self):
        """
        setups
        :return:
        """
        self.scene.set_program(self.program.get_program())
        self.scene.start()
        self.clock.tick()

    def run(self):
        self.blit()
        self.pause = True
        while True:
            self.blit()
            if self.scene.launch:
                self.scene.step(self.clock.tick())
                self.clock.tick()
                self.scene.update()

            self.event()

            if self.scene.done and not self.scene.success:
                print("And you failed :)")
                self.reload()
            pygame.display.flip()
            pygame.display.update()
            # TODO FPS LOCK

    def exit(self):
        self.pause = True
        pygame.quit()
        sys.exit()
