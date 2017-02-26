# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 24.02.2017


def decode(program):
    """
    Decodes program to simple commands. Decode LO and OP to pure commands:
    LO LEFT BACK OP => LEFT BACK LEFT BACK
    :param program: list of string
    :return:
    """
    result = []
    i = 0
    while i < len(program):
        if program[i] == "lo":
            lo = 1
            j = i + 1
            while lo > 0:
                if j == len(program):
                    program.append("op")

                if program[j] == "lo":
                    lo += 1
                elif program[j] == "op":
                    lo -= 1

                j += 1 if lo > 0 else 0
            if i + 1 == j - 1:
                tmp = [program[i + 1]]
            else:
                tmp = program[i + 1:j]
            del program[j]
            del program[i]
            program[i:i] = tmp
            i -= 1
        elif program[i] == "op":
            program[0:0] = ["lo"]
            i = 0
            result = []
        else:
            result.append(program[i])
        i += 1
    return result
