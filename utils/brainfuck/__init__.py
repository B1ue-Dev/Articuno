from .brainfuck import *


def evaluate(commands):
	interpreter = BrainfuckInterpreter(commands)
	while interpreter.available():
		interpreter.step()

	return interpreter.output.read()


__all__ = (
	'BrainfuckInterpreter'
)