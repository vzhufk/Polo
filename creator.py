# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 19.01.2017


import engine
import level


def change_voice():
    global current
    voice = level.Voice(current.name)
    say = input("Set language...")
    voice.lang = say
    try:
        voice.load()
    except FileNotFoundError:
        voice.save()
        voice.load()

    while True:
        say = int(input("(1) Add start phrase \n"
                        "(2) Add end phrase \n"
                        "(0) Exit\n>"))

        if say == 1:
            phrase = input("Set phrase for start...")
            voice.add_start(phrase)
        elif say == 2:
            phrase = input("Set phrase for end...")
            voice.add_end(phrase)
        else:
            break
    voice.save()


def delete_tile():
    global current
    print(">Delete...")
    x = input(">Set x...")
    y = input(">Set y...")
    current.delete_tile((int(x), int(y)))


def add_tile():
    # TODO Output field

    x = int(input(">Set x location\n>"))
    y = int(input(">Set y location\n>"))
    name = input(">Set type of tile: ('0' - default, '-1' - finish, 'custom_name' - custom) \n>")
    global current
    if int(name) == 0:
        current.add_tile((x, y))
    elif int(name) == -1:
        current.add_tile((x, y), "finish")
    else:
        current.add_tile((x, y), name)


def command_cfg():
    global current
    full = {
        "f": "forward",
        "b": "back",
        "rg": "right",
        "lf": "left",
        "lo": "lo",
        "op": "op"
    }
    command_name = ""
    while command_name not in full:
        command_name = input(">Set name of command: "
                             "\n( f - forward, b - back, lf - left, rg - right, lo - start loop, op - end of loop )\n>")
    amount = input(">Set amount\n")

    print(">Prev amount was " + str(current.moves[full[command_name]]) + "\n>")
    current.change_command(full[command_name], amount)


def robot_place():
    global current
    x = int(input(">Set x location\n>"))
    y = int(input(">Set y location\n>"))
    direction = int(input(">Set direction\n>"))
    current.robot_direct(direction)
    current.robot_place((x, y))


say = input(">Welcome to level creator!\n Create new (1) or Edit existing (2)?\n>")
name = input(">Name?\n>")

current = level.Level(name)
if int(say) == 2:
    current.load()

run = True
while run:
    say = input(">(1) Add tile\n"
                ">(2) Delete tile\n"
                ">(3) Change command\n"
                ">(4) Polo placement\n"
                ">(5) Add Voice\n"
                ">(0) Exit\n>")

    if int(say) == 1:
        add_tile()
    elif int(say) == 2:
        delete_tile()
    elif int(say) == 3:
        command_cfg()
    elif int(say) == 4:
        robot_place()
    elif int(say) == 5:
        change_voice()
    else:
        run = False

q = input(">Save?(1-0)\n>")
if int(q) == 1:
    current.save()
r = input(">Run?(1-0)\n>")
if int(r) == 1:
    e = engine.Engine()
    e.load(current.name)
    e.run()
