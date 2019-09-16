# -*- coding: utf-8 -*-

from json import load

from .helpers import _parse_paths
from .helpers import _parse_size
from .utils import pwrite


sep = '|'
compass = {
    'N': (0, -1),
    'n': (0, 1),
    'R': (1, 0),
    'r': (-1, 0),
    'Q': (-1, -1),
    'q': (1, 1),
    'E': (1, -1),
    'e': (-1, 1),
    'D': (0, 0, True),
    }

class Gridfont():
  def __init__(self, comp):
    self.jsn = {}
    self.compass = comp

  def _load(self, fn):
    with open(fn) as f:
      self.jsn = load(f)
    return self

  def parse(self, fn):
    print('parsing:', fn)
    self._load(fn)
    for char, o in self.jsn.items():
      raw_paths = o['raw'].split(sep)
      w, h = _parse_size(raw_paths[0])
      raw_paths = raw_paths[1:]
      assert raw_paths, 'must have at least one path'
      paths = list(_parse_paths(self.compass, raw_paths))
      assert paths, 'failed to parse at least one path'
      o['w'] = w
      o['h'] = h
      num = len(paths)
      print('char: {:s} --- w: {:d} h: {:d} # {:d}'.format(char, w, h, num))
      o['paths'] = paths
      o['num'] = num
    return self

  def save(self, fn):
    # from .utils import pprint
    # pprint(self.jsn)
    print('writing:', fn)
    with open(fn, 'w') as f:
      pwrite(self.jsn, f)
    return self

