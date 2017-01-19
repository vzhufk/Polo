# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 19.01.2017

import Modules.level
import engine
import level

say = input(">Welcome to level creator!\n Create new (1) or Edit existing (2)?\n>")
name = input(">Name?\n>")
current = level.Level(name)
if int(say) == 2:
    current.load()

run = True
while run:
    say = input(">(1) Add tile\n"
                ">(2) Change command\n"
                ">(0) Exit\n>")

    if int(say) == 1:
        x = int(input(">Set x location\n>"))
        y = int(input(">Set y location\n>"))
        name = input(">Set type of tile\n>")
        if name == "":
            current.add_tile((x, y))
        else:
            current.add_tile((x, y), name)
    elif int(say) == 2:
        name = input(">Set name of command\n>")
        amount = input(">Set amount\n")
        print(">Prev amount was " + str(current.moves[name]) + "\n>")
        current.change_command(name, amount)
    elif int(say) == 0:
        run = False

q = input(">Save?(1-0)\n>")
if int(q) == 1:
    current.save()
r = input(">Run?(1-0)\n>")
if int(r) == 1:
    e = engine.Engine()
    e.load(current.name)
    e.run()
