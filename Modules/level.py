# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 19.01.2017
import os
import pickle

import load
from robot import Robot

tile = (50, 50)
image_expansion = ".png"
location = "Levels/"
expansion = ""
tile_location = "Source/Tiles/"
tile_default = "default"
tile_expansion = ".png"


class RawTile:
    def __init__(self, kind, place):
        self.type = kind
        self.location = tile_location + kind + tile_expansion
        self.place = place


class Level:
    def __init__(self, name):
        self.name = name
        self.tiles = []
        self.moves = {'right': 0, 'left': 0, 'forward': 0, 'back': 0, 'lo': 0, 'op': 0}
        self.placement = (1, 1)
        self.direction = 2

    def load(self):
        f = open(location + self.name + expansion, 'rb')
        tmp_dict = pickle.load(f)
        f.close()

        self.__dict__.update(tmp_dict)

    def save(self):
        f = open(location + self.name + expansion, 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()

    def add_tile(self, place, name=tile_default):
        if os.path.exists(tile_location + name + tile_expansion):
            self.tiles.append(RawTile(name, (place[0] * tile[0], place[1] * tile[1])))

    def change_command(self, name, amount):
        self.moves[name] = int(amount)

    def robot_place(self, t):
        self.placement = (t[0], t[1])

    def robot_direct(self, d):
        self.direction = d
