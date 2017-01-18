import os
import pickle
import sys

import pygame

import varibles
from Modules.controls import Controls
from Modules.program import Program
from scene import Scene

FPS = varibles.FPS
window_title = varibles.window_title
screen_resolution = varibles.screen_resolution
screen_mode = varibles.screen_mode


class Engine:
    def __init__(self):
        pygame.init()
        self.running = True
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)
        pygame.display.set_caption(window_title)
        self.display = pygame.display.set_mode(screen_resolution)
        self.level = {}
        self.controls = Controls()
        self.program = Program()
        self.scene = Scene("demo")

    def import_level(self, name):
        file = open(name, 'rb')

        self.level = pickle.load(file)

    def export_level(self, name):
        file = open(name, 'wb')

        tmp = [['flor', (0, 0)],
               ['flor', (0, 1)]]

        pickle.dump(tmp, file)

    def blit(self):
        self.display.blit(self.controls, self.controls.position)
        self.display.blit(self.program, self.program.position)
        self.display.blit(self.scene, self.scene.position)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if pygame.mouse.get_pressed()[0]:
                self.controls.event(pygame.mouse)
                self.program.event(pygame.mouse)

                if self.controls.get_command() != "":
                    self.program.add(self.controls.get_command())
                if self.program.get_deleted() != "":
                    self.controls.add(self.program.get_deleted())

                self.blit()

    def run(self):
        self.blit()
        while self.running:
            self.event()

            pygame.display.flip()
            pygame.display.update()
            # TODO FPS LOCK
            # TODO GIT IT
