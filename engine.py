import os
import sys

import pygame

import Libraries.load as load
import sprite
import varibles
from Modules.controls import Controls
from Modules.menu import Menu
from Modules.program import Program
from Modules.scene import Scene
from level import Level
from message import Message

FPS = varibles.FPS
window_title = varibles.window_title
screen_resolution = varibles.screen_resolution
screen_mode = varibles.screen_mode


class Engine:
    def __init__(self):
        pygame.init()
        # Engine pause
        self.pause = False
        # Intro
        self.alert = True
        # Set up of window
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)
        # Window title
        pygame.display.set_caption(window_title)
        # Set up window resolution
        self.display = pygame.display.set_mode(screen_resolution)  # pygame.FULLSCREEN
        # Sets level
        self.current_level = 1
        # Clock init for ticks
        self.clock = pygame.time.Clock()
        # Level load
        self.level = Level(load.get_levels()[self.current_level])
        # Sound
        self.sound = True
        self.controls = Controls()
        self.program = Program()
        self.scene = Scene()
        self.menu = Menu()
        self.message = Message()

    def update_all(self):
        """
        Updating all screen.
        :return:
        """
        self.display.blit(self.controls, self.controls.rect)
        self.display.blit(self.program, self.program.rect)
        self.display.blit(self.scene, self.scene.rect)

        if self.pause:
            self.display.blit(self.menu, self.menu.rect)
            # TODO Maybe Blur effect in pause
        if self.alert:
            self.display.blit(self.message, self.message.rect)
        pygame.display.flip()

    def update(self):
        """
        Updating parts of scene
        :return:
        """
        mouse = pygame.mouse.get_pos()
        if self.alert:
            self.display.blit(self.message, self.message.rect)
            pygame.display.update(self.message.rect)
        elif self.pause:
            self.display.blit(self.menu, self.menu.rect)
            pygame.display.update(self.menu.rect)
        else:
            if self.program.is_in(mouse) or self.controls.is_in(mouse):
                self.display.blit(self.controls, self.controls.rect)
                self.display.blit(self.program, self.program.rect)
                pygame.display.update(self.program.rect)
                pygame.display.update(self.controls.rect)
            if self.scene.is_in(mouse) or self.scene.launch:
                self.display.blit(self.scene, self.scene.rect)
                pygame.display.update(self.scene.rect)

    def get_level(self):
        """
        Returns current level
        :return:
        """
        return self.current_level

    def set_level(self, new_lvl):
        """
        Set level
        :param new_lvl: int index of level in list
        :return:
        """
        self.current_level = new_lvl
        self.load(load.get_levels()[new_lvl])
        self.update_all()

    def load(self, name):
        """
        Load level to all modules
        :param name:
        :return:
        """
        self.level = Level(name)
        self.level.load()
        # Pass level to other modules
        self.program = Program()
        self.controls.level(self.level)
        self.scene.level(self.level)
        # For direct moves
        self.program.direction = int(self.scene.robot.direction)
        # self.update_all()

    # Add sound handler. All sounds plays here.
    def check_sound(self):
        # TODO Mute sound in all modules
        if self.sound:
            pygame.mixer.unpause()
        else:
            pygame.mixer.pause()

    def reload(self):
        """
        Reloads level(scene)
        :return:
        """
        self.scene.level(self.level)
        self.update_all()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.alert:
                        self.alert = False
                        self.pause = True
                    else:
                        self.pause = not self.pause
                        self.update_all()

            if self.pause:
                self.menu.event(pygame.mouse)
            else:
                if not self.scene.launch:
                    self.controls.event(pygame.mouse)
                    self.program.event(pygame.mouse)
                    self.scene.event(pygame.mouse)

                # I can just change time in scene to speed up
                if self.scene.launch and pygame.mouse.get_pressed()[0]:
                    # Speed up scene
                    self.scene.speed_up = True
            self.invoker()

    def invoker(self):
        """
        Invokes module calls
        :return:
        """
        """Controls Echos"""
        if self.controls.get_echo() is not None:
            self.program.add(self.controls.get_echo())
            # Direct turn
            self.controls.set_delta_direct(self.program.get_delta_direction())
            self.controls.echo_out()

        """Program Echos"""
        if self.program.get_echo() is not None:
            self.controls.add(self.program.get_echo())
            # Direct turn
            self.controls.set_delta_direct(self.program.get_delta_direction())
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
            if str(i) == "play":
                self.pause = False
            elif str(i) == "exit":
                self.exit()
            elif str(i) == "choose":
                self.load(i.caption)
                self.update_all()
            elif str(i) == "sound":
                self.sound = i.switch_index == 1
                self.check_sound()
            elif str(i) == "about":
                varibles.about()

    def scene_handler(self):
        for i in self.scene.echo:
            if i.name == "finish":
                self.pause = True
            elif i.name == "polo":
                self.setup_scene()

    def setup_intro(self):
        tmp = sprite.Sprite()
        tmp.load_image("Source/logo.png", (0, 0, 0))
        tmp.image = tmp.image.convert_alpha()
        self.message.group.add(tmp)
        self.message.update()

    def setup_scene(self):
        """
        setups
        :return:
        """
        self.scene.set_program(self.program.get_program())
        self.scene.start()
        self.clock.tick()

    def run(self):
        self.pause = True
        self.clock.tick()

        # Intro
        self.setup_intro()
        while self.alert:
            self.message.step(self.clock.tick(FPS))
            self.message.update()
            self.alert = self.message.launch
            self.update()
            self.event()

        self.update_all()

        while True:

            if self.scene.launch:
                self.scene.step(self.clock.tick(FPS))
                self.scene.update()
            self.event()

            if self.scene.done and not self.scene.success:
                print("And you failed :)")
                self.reload()
            elif self.scene.done and self.scene.success:
                print("WP")
                self.reload()
                self.pause = True

            self.update()

    def exit(self):
        self.pause = True
        pygame.quit()
        sys.exit()
