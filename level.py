# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 19.01.2017
import io
import os
import pickle

import variables

tile = (50, 50)
image_expansion = ".png"
location = "Levels/"
expansion = ""
tile_location = "Source/Tiles/"
tile_default = "default"
tile_expansion = ".png"


# TODO Add Messages
# TODO Some refactor thing


class RawTile:
    """
    Raw tile class
    Because Tile that extends pygame.sprite cant be pickled
    """

    def __init__(self, kind, place):
        self.type = kind
        self.location = tile_location + kind + tile_expansion
        self.place = place


class Level:
    def __init__(self, name):
        # Level name
        self.name = name
        # List of tiles
        self.tiles = []
        # Available commands and amount
        self.moves = {'right': 0, 'left': 0, 'forward': 0, 'back': 0, 'lo': 0, 'op': 0}
        # Robot placement
        self.placement = (1, 1)
        self.direction = 2

    def load(self):
        """
        Loads level from file
        :return:
        """
        f = open(location + self.name + expansion, 'rb')
        tmp_dict = pickle.load(f)
        f.close()

        self.__dict__.update(tmp_dict)

    def save(self):
        """
        Saves level
        :return:
        """
        f = open(location + self.name + expansion, 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()

    def delete_tile(self, place):
        """
        Deletes tile at some place
        :param place: tuple
        :return: 
        """
        place = (place[0] * tile[0], place[1] * tile[1])
        for i in self.tiles:
            if i.place == place:
                self.tiles.pop(self.tiles.index(i))

    def add_tile(self, place, name=tile_default):
        """
        Add new tile on scene
        :param place: where
        :param name: name/type of tile
        :return:
        """
        if os.path.exists(tile_location + name + tile_expansion):
            self.tiles.append(RawTile(name, (place[0] * tile[0], place[1] * tile[1])))

    def change_command(self, name, amount):
        """
        Changes some command available amount
        :param name: name of command
        :param amount: new amount
        :return:
        """
        self.moves[name] = int(amount)

    def robot_place(self, t):
        """
        Place robot on tile
        :param t: tuple of (x, y) tile
        :return:
        """
        self.placement = (t[0], t[1])

    def robot_direct(self, d):
        """
        Direct robot    
        :param d: 0<=d<=3 Direction
        :return:
        """
        self.direction = d

        # TODO Add str method and use it in creator


class Voice:
    def __init__(self, level_name="", lang="en"):
        self.name = level_name
        self.lang = lang
        self.start = []
        self.end = []

    def add_start(self, text):
        self.start.append(text)

    def add_end(self, text):
        self.end.append(text)

    def load(self):
        """
        Loads level from file
        :return:
        """
        try:
            with io.open(location + self.lang + "/" + self.name + expansion, 'r', encoding='utf-8') as f:
                # tmp_dict = pickle.load(f)
                # f.close()
                # self.__dict__.update(tmp_dict)
                s = str(f.read())
                for i in s.split("\n"):
                    if i[0] == "+":
                        self.end.append(i[1:])
                    elif i[0] == "-":
                        self.start.append(i[1:])
                f.close()

        except FileNotFoundError:
            pass

    # TODO Refactor
    def save(self):
        """
        Saves level
        :return:
        """
        with io.open(location + self.lang + "/" + self.name + expansion, 'w', encoding='utf-8') as f:
            # pickle.dump(self.__dict__, f, 2)
            for i in self.start:
                f.write("-" + i)
            for i in self.end:
                f.write("+" + i)
            f.close()


def save_current_level(index):
    f = open(variables.user_config_file, "w")
    f.write(str(int(index)))
    f.close()


def load_current_level():
    f = open(variables.user_config_file, "r")
    index = int(f.read())
    f.close()
    return index
