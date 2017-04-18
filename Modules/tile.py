# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 19.01.2017
from Modules.sprite import Sprite

location = "Source/Tiles/"
expansion = ".png"


class Tile(Sprite):
    def __init__(self, name, placement=(0, 0), image_path=None):
        """
        :param name: Tile name of type
        :param placement: Tile position
        :param image_path: Path to tile image
        """
        Sprite.__init__(self, name, placement)
        image_path = image_path if image_path is not None else location + name + expansion
        self.load_image(image_path)