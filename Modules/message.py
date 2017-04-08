# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 08.04.2017

import surface
import varibles

position = (125, 125)
size = (varibles.screen_resolution[0] - position[0], varibles.screen_resolution[1] - position[1])
time = 2000
color = (0, 0, 0)
sec_color = (106, 106, 106)


class Message(surface.Surface):
    def __init__(self, pos=position, s=size, t=time):
        self.full_time = t
        self.time = t
        self.alpha = 12
        self.launch = True
        surface.Surface.__init__(self, pos, s, color)
        self.set_colorkey(color)

    def update(self):
        surface.Surface.update(self)

    # fade fucking out
    def step(self, tick):
        self.time -= tick
        self.alpha = self.time / self.full_time * 225
        self.launch = self.time > 0
        self.set_alpha(int(self.alpha))
