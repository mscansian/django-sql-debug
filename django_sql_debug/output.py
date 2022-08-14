import math
import os
import sys
from shutil import get_terminal_size

from django.conf import settings

header_size = getattr(settings, 'SQL_DEBUG_OUTPUT_SIZE', get_terminal_size()[0])
output_stream = getattr(settings, 'SQL_DEBUG_OUTPUT_STREAM', sys.stdout)


def write_header(text, left, right, color=None):
    left_size = math.floor((header_size-len(text)-2)/2)
    right_size = header_size - left_size - len(text) - 2
    write(' '.join([
        left*math.floor(left_size/len(left)),
        text,
        right*math.floor(right_size/len(right)),
    ]), color=color)


def write(text, color=None):
    if color:
        output_stream.write(color)
    output_stream.write(str(text))
    output_stream.write(os.linesep)
