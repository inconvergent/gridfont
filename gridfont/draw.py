# -*- coding: utf-8 -*-

from svgwrite import Drawing

black = 'black'
accent = 'cyan'


def _shift(path, pad):
  sx, sy = pad
  for x, y in path:
    yield x+sx, y+sy


def _svgiter(path):
  yield 'M{},{} '.format(*path[0])
  for p in path[1:]:
    yield 'L{},{} '.format(*p)

def tosvgpath(path, pad=(0, 0), closed=False):
  res = ''.join(_svgiter(list(_shift(path, pad)))).strip()
  if closed:
    return '{:s}Z'.format(res)
  return res


def _box(bbox):
  w, h = bbox
  return [[0, 0], [w, 0], [w, h], [0, h]]


def draw_paths(fn, bbox, paths, pad=(0, 0), sw=0.1):
  w, h = bbox
  sx, sy = pad
  dwg = Drawing(str(fn), size=(w+2*sx, h+2*sy), profile='tiny', debug=False)

  bbox_path = tosvgpath(_box(bbox), pad, closed=True)
  dwg.add(dwg.path(d=bbox_path, stroke=accent, stroke_width=sw, fill='none'))

  for path in paths:
    dwg.add(
        dwg.path(
            d=tosvgpath(path, pad),
            stroke=black,
            fill='none',
            stroke_width=sw))
  dwg.save(pretty=True, indent=2)

