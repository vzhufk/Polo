import os
from os.path import isfile, join, isdir

import pygame

import variables


def image(name, color_key=None):
    fullname = os.path.join('', name)
    try:
        current = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', name)
        current = pygame.surface.Surface((50, 50))
        current.fill((255, 0, 0))
        return current, current.get_rect()
    current = current.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = current.get_at((0, 0))
        current.set_colorkey(color_key, pygame.RLEACCEL)
    return current, current.get_rect()


def load_lined_sprite(filename, w, h):
    images = []
    parent_image = pygame.image.load(os.path.join('src', filename)).convert_alpha()

    parent_image.set_colorkey((255, 0, 255))
    parent_w, parent_h = parent_image.get_size()

    for i in range(int(parent_w / w)):
        images.append(parent_image.subsurface((i * w, 0, w, h)))

    return images


def load_sliced_sprite(filename, w, h):
    images = []
    parent_image = pygame.image.load(filename).convert_alpha()

    parent_image.set_colorkey((255, 0, 255))
    parent_w, parent_h = parent_image.get_size()

    for j in range(int(parent_h / h)):
        for i in range(int(parent_w / w)):
            images.append(parent_image.subsurface((i * w, j * h, w, h)))
    return images


def sound(name):
    class NoneSound:
        def play(self): pass

    if not pygame.mixer:
        return NoneSound()
    fullname = name
    try:
        current_sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound:', name)
    return current_sound


def get_levels(path=variables.level_path):
    path = os.getcwd() + path
    return [f for f in os.listdir(path) if isfile(join(path, f))]


def get_languages(path=variables.level_path):
    path = os.getcwd() + path
    return [f for f in os.listdir(path) if isdir(join(path, f))]
