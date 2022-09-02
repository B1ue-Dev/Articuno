# credits:
# - https://github.com/sstelian/Text-to-Brainfuck/blob/master/brainfuck_generator.py
# - https://github.com/redevined/brainfuck/blob/master/brainfuck.py

import sys


def char_to_bf(char):
    buffer = "[-]>[-]<"
    for i in range(ord(char) // 10):
        buffer = buffer + "+"
    buffer = buffer + "[>++++++++++<-]>"
    for i in range(ord(char) % 10):
        buffer = buffer + "+"
    buffer = buffer + ".<"
    return buffer


def delta_to_bf(delta):
    buffer = ""
    for i in range(abs(delta) // 10):
        buffer = buffer + "+"

    if delta > 0:
        buffer = buffer + "[>++++++++++<-]>"
    else:
        buffer = buffer + "[>----------<-]>"

    for i in range(abs(delta) % 10):
        if delta > 0:
            buffer = buffer + "+"
        else:
            buffer = buffer + "-"
    buffer = buffer + ".<"
    return buffer


def string_to_bf(string, commented):
    buffer = ""
    if string is None:
        return buffer
    for i, char in enumerate(string):
        if i == 0:
            buffer = buffer + char_to_bf(char)
        else:
            delta = ord(string[i]) - ord(string[i - 1])
            buffer = buffer + delta_to_bf(delta)
        if commented:
            buffer = buffer + " " + string[i].strip("+-<>[],.") + "\n"
    return buffer


def precompute_jumps(program):
    stack = []
    ret = {}

    pc = 0

    while not pc == len(program):
        opcode = program[pc]
        if opcode == "[":
            stack.append(pc)
        elif opcode == "]":
            target = stack.pop()
            ret[target] = pc
            ret[pc] = target
        pc += 1

    return ret


def interpret_bf(code):
    buffer = [0]
    jump_map = precompute_jumps(code)

    ptr = 0
    pc = 0
    result = ""

    while not pc == len(code):
        opcode = code[pc]
        if opcode == ">":
            ptr += 1
            if ptr == len(buffer):
                buffer.append(0)
        elif opcode == "<":
            ptr -= 1
        elif opcode == "+":
            buffer[ptr] += 1
        elif opcode == "-":
            buffer[ptr] -= 1
        elif opcode == ".":
            result += chr(buffer[ptr])
        elif opcode == ",":
            buffer[ptr] = ord(sys.stdin.read(1))
        elif opcode == "[":
            if buffer[ptr] == 0:
                pc = jump_map[pc]
        elif opcode == "]":
            if buffer[ptr] != 0:
                pc = jump_map[pc]
        pc += 1

    return result


class Brainfuckery:
    def __init__(self):
        pass

    def convert(self, string):
        return string_to_bf(string, False)

    def interpret(self, code):
        return interpret_bf(code)
