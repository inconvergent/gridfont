# -*- coding: utf-8 -*-

from svgwrite import Drawing
from svgwrite import rgb

black = rgb(0, 0, 0, '%')
accent = rgb(0, 100, 100, '%')


def _shift(path, sx=1, sy=1):
  for x, y in path:
    yield x+sx, y+sy


def _svgpath(path):
  yield 'M{:d},{:d} '.format(*path[0])
  for p in path[1:]:
    yield 'L{:d},{:d} '.format(*p)

def svgpath(path, closed=False):
  res = ''.join(_svgpath(list(_shift(path)))).strip()
  if closed:
    return '{:s}Z'.format(res)
  return res


def _box(bbox):
  w, h = bbox
  return [[0, 0], [w-1, 0], [w-1, h-1], [0, h-1]]


def draw_paths(fn, bbox, paths):
  w, h = bbox
  dwg = Drawing(fn, size=(w+2, h+2), profile='tiny')

  bbox_path = svgpath(_box(bbox), closed=True)
  dwg.add(dwg.path(d=bbox_path, stroke=accent, stroke_width=0.1, fill='none'))

  for path in paths:
    dwg.add(dwg.path(
        d=svgpath(path),
        stroke=black,
        fill='none',
        stroke_width=0.2))
  dwg.save(pretty=True, indent=2)

