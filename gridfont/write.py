#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from json import load

from svgwrite import Drawing

from helpers import _rel_move
from draw import tosvgpath
from draw import black


def shift_path(path, s):
  sx, sy = s
  for x, y in path:
    yield (x + sx, y + sy)


class Writer():
  def __init__(self, fn, size, pad=0):
    self.pos = (pad, pad)
    self.pad = pad
    self.space = 2
    self.nl = 12
    self.dwg = Drawing('tmp.svg', size=size, profile='tiny', debug=False)
    with open(str(fn), 'r') as f:
      self.jsn = load(f)

  def newline(self):
    self.pos = (self.pad, self.pos[1] + self.nl)

  def write(self, phrase):
    for s in phrase:
      if s == ' ':
        self.pos = _rel_move(self.pos, self.space)
      elif s in self.jsn:
        o = self.jsn[s]
        gw = o['w']
        gh = o['h']
        paths = o['paths']
        for path in paths:
          self.dwg.add(
              self.dwg.path(
                  d=tosvgpath(list(shift_path(path, self.pos))),
                  stroke=black,
                  fill='none',
                  stroke_width=0.2))
        self.pos = _rel_move(self.pos, (gw + self.space, 0))

      else:
        print('symbol not found: {:s}'.format(s))
    self.dwg.save(pretty=True, indent=2)


def main():
  phrases = [
      'abcdefghij',
      'klmnopqrst',
      'uvwxyz',
      '0123456789',
      '!()[]+*-?,',
      '.\:;/='
      ]


  writer = Writer('../out/res.json', (100, 100), pad=2)

  for phrase in phrases:
    writer.write(phrase)
    writer.newline()


if __name__ == '__main__':
  main()
