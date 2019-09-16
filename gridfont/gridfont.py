# -*- coding: utf-8 -*-

from json import load

from .helpers import _parse_paths
from .helpers import _parse_size
from .utils import pwrite


SEP = '|'


def assert_symbol_size(w, h, paths):
  for path in paths:
    for x, y in path:
      assert 0 <= x <= w, 'x is out of bounds'
      assert 0 <= y <= h, 'y is out of bounds'

class Gridfont():
  def __init__(self, comp):
    self.jsn = {}
    self.groups = {}
    self.symbols = {}
    self.compass = comp

  def _load(self, fn):
    with open(fn) as f:
      jsn = load(f)
      # note: these structures are manipulated in place
      self.jsn = jsn
      self.groups = jsn['groups']
      self.symbols = jsn['symbols']
    return self

  def parse(self, fn):
    print('parsing:', fn)
    self._load(fn)

    for char, o in self.symbols.items():
      try:
        raw = o['raw'].strip()
        raw_paths = raw.split(SEP)
        w, h = _parse_size(raw_paths[0])
        raw_paths = raw_paths[1:]
        assert raw_paths, 'must have at least one path'
        paths = list(_parse_paths(self.compass, raw_paths))
        assert paths, 'failed to parse at least one path'
        assert_symbol_size(w, h, paths)
        o['w'] = w
        o['h'] = h
        num = len(paths)
        print('char: {:s} --- w: {:d} h: {:d} # {:d}'.format(char, w, h, num))
        o['paths'] = paths
        o['num'] = num
      except Exception as e:
        print('error char: {:s} --- {:s}'.format(char, str(e)))
    return self

  def save(self, fn):
    print('writing:', fn)
    with open(fn, 'w') as f:
      pwrite(self.symbols, f)
    return self

