#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""gridfont

Usage:
  gridfont parse <in> <out> [--lenient] [--svg]
  gridfont write <in> <out> <text>

Options:

  --svg       export an svg for each symbol
  --lenient   ignore some tests/asserts, most notably the out of bounds test

  -h --help   show this screen.
  --version   show version.


Examples:
  gridfont parse input_file.json output_path
  gridfont write parsed.json tmp.svg 'my text'
"""


__ALL__ = ['Gridfont']

from pathlib import Path
import sys
import traceback

from docopt import docopt

from .gridfont import Gridfont
from .write import Writer


def main():
  args = docopt(__doc__, version='gridfont 0.5.2')
  try:
    _in = Path(args['<in>'])
    _out = Path(args['<out>'])
    print(args)

    # parse a symbol definition
    if args['parse']:
      font = Gridfont(_in).parse(lenient=args['--lenient'])
      font.save(_out)
      if args['--svg']:
        font.scale(20)
        font.save_svg(_out, pad=(2, 2), sw=2)

    # write a phrase as SVG
    elif args['write']:
      writer = Writer(_in, _out, (4000, 4000), pad=80, xdst=40, nl=10*40, sw=7)
      writer.scale(40)
      for line in args['<text>'].split('\n'):
        writer.write(line)
        print(line)
        writer.newline()
    else:
      print('use gridfont --help to see usage')

  except Exception:
    traceback.print_exc(file=sys.stdout)
    exit(1)


if __name__ == '__main__':
  main()

