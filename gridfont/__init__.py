#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""gridfont

Usage:
  gridfont <in> <out>

Options:

  -h --help   show this screen.
  --version   show version.

Examples:
  gridfont
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
    font = Gridfont(_in).parse().save(_out)

  except Exception:
    traceback.print_exc(file=sys.stdout)
    exit(1)


if __name__ == '__main__':
  main()

