#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from json import load

from svgwrite import Drawing

from .helpers import _rel_move
from .draw import tosvgpath
from .draw import black


def shift_path(path, s):
  sx, sy = s
  for x, y in path:
    yield (x + sx, y + sy)


class Writer():
  def __init__(self, fontfn, outfn, size, pad=0, sw=0.2, nl=10):
    self.pos = (pad, pad)
    self.sw = sw
    self.pad = pad
    self.nl = nl
    self.xdst = 1
    self.dwg = Drawing(str(outfn), size=size, profile='tiny', debug=False)
    with open(str(fontfn), 'r') as f:
      self.symbols = load(f)['symbols']

  def newline(self):
    self.pos = (self.pad, self.pos[1] + self.nl)

  def write(self, phrase):
    for s in phrase:
      if s in self.symbols:
        o = self.symbols[s]
        gw = o['w']
        paths = o['paths']
        for path in paths:
          self.dwg.add(
              self.dwg.path(
                  d=tosvgpath(list(shift_path(path, self.pos))),
                  stroke=black,
                  fill='none',
                  stroke_width=self.sw))
        self.pos = _rel_move(self.pos, (gw + self.xdst, 0))
      else:
        print('symbol not found: {:s}'.format(s))
    self.dwg.save(pretty=True, indent=2)

