# -*- coding: utf-8 -*-

from json import load

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
      self.jsn = jsn
      self.groups = jsn['groups']
      self.symbols = jsn['symbols']
      self.compass = jsn['compass']

      cmd = _get_all_commands(self.compass, list(self.special.values()))
      self.all_commands = cmd

      # path definition tokenizer
      self.tokfx = _get_tokenizer(cmd)
    return self

  # TODO: restructure this?
  def _do_cmd(self, state, bbox, cmd, arg):
    if cmd == self.special['abs_move']:
      return arg[0], arg[1], state[-1]
    if cmd == self.special['pen_down']:
      return state[0], state[1], True

    if cmd == self.special['left']:
      return 0, state[1], state[-1]
    if cmd == self.special['right']:
      return state[0], bbox[0]-1, state[-1]

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

  def parse(self):
    print('parsing ...')
    for symb, o in self.symbols.items():
      try:
        raw = o['raw']
        info, raw_paths = raw.strip().split(':')
        print('symb: {:s} {:s}'.format(symb, raw))
        path_strings = list([r.strip() for r in raw_paths.strip().split('|')])
        assert path_strings, 'must have at least one path'
        w, h = _parse_info(info)
        paths = list(self._parse_paths((w, h), path_strings))
        assert paths, 'failed to parse at least one path'
        _assert_symbol_size(w, h, paths)
        o['w'] = w
        o['h'] = h
        o['paths'] = paths
        o['num'] = len(paths)
        print('        w {:d} h {:d} # {:d}'.format(w, h, len(paths)))
      except Exception as e:
        print('symb error: {:s} --- {:s}'.format(symb, str(e)))
    return self

  def save(self, fn):
    print('writing:', fn)
    with open(fn, 'w') as f:
      pwrite(self.symbols, f)
    return self

