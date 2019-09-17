#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""gridfont

Usage:
  gridfont <in> <out> [--lenient]

Options:

  --lenient   ignore some asserts

  -h --help   show this screen.
  --version   show version.


Examples:
  gridfont input_file.json output_path
"""


__ALL__ = ['Gridfont']

import sys
import traceback

from docopt import docopt

from .gridfont import Gridfont



def main():
  args = docopt(__doc__, version='gridfont 0.0.1')
  try:
    _in = args['<in>']
    _out = args['<out>']
    font = Gridfont(_in).parse(lenient=args['--lenient']).save(_out)
    font.save_svg(_out)

  except Exception:
    traceback.print_exc(file=sys.stdout)
    exit(1)


if __name__ == '__main__':
  main()

