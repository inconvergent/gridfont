# -*- coding: utf-8 -*-

from json import load

from .draw import draw_paths
from .helpers import _assert_symbol_size
from .helpers import _assert_valid_cmds
from .helpers import _get_all_commands
from .helpers import _get_tokenizer
from .helpers import _parse_info
from .helpers import _proc_tok
from .helpers import _rel_move
from .utils import pwrite


class Gridfont():
  def __init__(self, fn):
    print('loading:', fn)
    self._load(fn)

  def _load(self, fn):
    with open(fn) as f:
      jsn = load(f)
      self.special = jsn['special']

      # note: these structures are manipulated in place
      self.groups = jsn['groups']
      self.symbols = jsn['symbols']
      self.compass = jsn['compass']

      cmd = _get_all_commands(self.compass, list(self.special.values()))
      self.all_commands = cmd

      # path definition tokenizer
      self.tokfx = _get_tokenizer(cmd)
    return self

  def _do_cmd(self, state, bbox, cmd, arg):
    if cmd == self.special['abs_move']:
      return arg[0], arg[1], state[-1]
    if cmd == self.special['pen_down']:
      return state[0], state[1], True

    # move x
    if cmd == self.special['left']:
      return 0, state[1], state[-1]
    if cmd == self.special['right']:
      return bbox[0]-1, state[1], state[-1]

    # move y
    if cmd == self.special['top']:
      return state[0], 0, state[-1]
    if cmd == self.special['bottom']:
      return state[0], bbox[1]-1, state[-1]

    if cmd in self.compass:
      npx, npy = _rel_move(state, self.compass[cmd], arg)
      return npx, npy, state[-1]

    raise ValueError('encountered invalid command.')

  def _parse_path(self, bbox, path):
    state = (0, 0, False)
    _assert_valid_cmds(self.all_commands, path)
    for tok in self.tokfx(path):
      cmd, arg = _proc_tok(tok)
      state = self._do_cmd(state, bbox, cmd, arg)
      x, y, pen = state
      if pen:
        yield x, y

  def _parse_paths(self, bbox, paths):
    for path in paths:
      yield list(self._parse_path(bbox, path))

  def parse(self, lenient=False):
    print('parsing ...')
    for symb, o in self.symbols.items():
      try:
        raw = o['raw']
        info, raw_paths = raw.strip().split(':')
        w, h = _parse_info(info)
        o['gw'] = w
        o['gh'] = h
        o['w'] = w-1
        o['h'] = h-1
        print('symb: {:s} {:s}'.format(symb, raw))
        path_strings = list([r.strip() for r in raw_paths.strip().split('|')])
        assert path_strings, 'definition must have at least one path'
        paths = list(self._parse_paths((w, h), path_strings))
        for p in paths:
          assert p, 'at least one path is empty, did you forget D?'
        if not lenient:
          _assert_symbol_size(w, h, paths)
        o['paths'] = paths
        o['num'] = len(paths)
        o['ord'] = ord(symb)
        print('  --> w {:d} h {:d} # {:d}'.format(w, h, len(paths)))
      except Exception as e:
        print('symb error: {:s} --- {}'.format(symb, e))
    return self

  def scale(self, s):
    # TODO: don't scale inplace?
    for o in self.symbols.values():
      w = o['w']
      h = o['h']
      new_paths = []
      for path in o['paths']:
        new_path = []
        for x, y in path:
          xx = s*(x-w*0.5)+w*0.5*s
          yy = s*(y-h*0.5)+h*0.5*s
          new_path.append((xx, yy))
        new_paths.append(new_path)
      o['w'] = w*s
      o['h'] = h*s
      o['paths'] = new_paths
    return self

  def save_svg(self, out, pad=(0, 0), sw=0.1):
    print('writing svgs to:', out)
    for symb, o in self.symbols.items():
      name = o['name'] if 'name' in o else symb
      _type = o['type'] if 'type' in o else 'symb'
      fn = out.joinpath('{:s}_{:s}.svg'.format(_type, name))
      try:
        draw_paths(fn, (o['w'], o['h']), o['paths'], pad, sw=sw)
      except Exception as e:
        print('svg err on symb: {:s}: {}'.format(symb, e))
    return self

  def save(self, out):
    fn = out.joinpath('res.json')
    print('writing:', fn)
    with open(str(fn), 'w') as f:
      pwrite(self.symbols, f)
    return self

