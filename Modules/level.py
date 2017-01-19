# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 19.01.2017
import pickle

import load

tile = (50, 50)
image_expansion = ".png"
location = "Levels/"
expansion = ""


class Tile:
    def __init__(self, kind, place):
        self.type = kind
        self.place = place


class Level:
    def __init__(self, name):
        self.name = name
        self.tiles = []
        self.moves = {'right': 0, 'left': 0, 'forward': 0, 'back': 0, 'lo': 0, 'op': 0}

    def load(self):
        f = open(location + self.name + expansion, 'rb')
        tmp_dict = pickle.load(f)
        f.close()

        self.__dict__.update(tmp_dict)

    def save(self):
        f = open(location + self.name + expansion, 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()

    def add_tile(self, name, place):
        try:
            tmp = load.image(name + image_expansion)
        finally:
            self.tiles.append(Tile(name, (place[0] / tile[0], place[1] / tile[1])))

    def change_command(self, name, amount):
        self.moves[name] = int(amount)
