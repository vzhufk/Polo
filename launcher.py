# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 20.01.2017
from os import listdir
from tkinter import *
from tkinter.ttk import Combobox

from os.path import isfile, join

import engine

level_path = "Levels/"

frame = Tk()

levels_label = Label(frame, text="Level:")
levels_label.place(x=25, y=0)

levels = Combobox(frame)
levels_names = []
for f in listdir(level_path):
    if isfile(join(level_path, f)):
        levels_names.append(f)
levels['values'] = levels_names
levels.set(levels_names[0])
levels.place(x=25, y=25)


def run_command(level=levels.get()):
    e = engine.Engine()
    e.load(level)
    e.run()


run = Button(frame, text="Run", command=run_command)
run.place(x=25, y=50)

edit = Button(frame, text="Edit")
edit.place(x=75, y=50)

q = Button(frame, text="Quit", command=quit)
q.place(x=125, y=50)

frame.mainloop()
