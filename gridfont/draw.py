# -*- coding: utf-8 -*-

from svgwrite import Drawing
from svgwrite import rgb

black = rgb(0, 0, 0, '%')

def shift(path):
  for x, y in path:
    yield x+1, y+1


def _svgpath(path):
  yield 'M{:d},{:d} '.format(*path[0])
  for p in path[1:]:
    yield 'L{:d},{:d}'.format(*p)


def draw_paths(fn, bbox, paths):
  w, h = bbox
  dwg = Drawing(fn, size=(w+2, h+2), profile='tiny')
  for path in paths:
    dwg.add(dwg.path(
        d=''.join(_svgpath(list(shift(path)))),
        stroke=black,
        fill='none',
        stroke_width=0.2))
  dwg.save()

