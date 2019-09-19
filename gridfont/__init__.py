#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""gridfont

Usage:
  gridfont parse <in> <out> [--lenient] [--svg]
  gridfont write <in> <out> <text>

Options:

  --svg       export an svg for each symbol
  --lenient   ignore some asserts

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
  args = docopt(__doc__, version='gridfont 0.1.1')
  try:
    _in = Path(args['<in>'])
    _out = Path(args['<out>'])

    # parse a symbol definition
    if args['parse']:
      font = Gridfont(_in).parse(lenient=args['--lenient']).save(_out)
      if args['--svg']:
        font.scale(20)
        font.save_svg(_out, pad=(2, 2), sw=2)

    elif args['write']:
      writer = Writer(_in, _out, (100, 100), pad=2)
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

