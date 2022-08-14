import math

from shutil import get_terminal_size


terminal_size = get_terminal_size()[0]


def print_header(text, left, right, color=None):
    left_size = math.floor((terminal_size-len(text))/2) - 1
    right_size = terminal_size - left_size - len(text)
    if color:
        print(color, end='')
    print(
        left*math.floor(left_size/len(left)),
        text,
        right*math.floor(right_size/len(right)),
    )

def print_line(text):
    print(text)
