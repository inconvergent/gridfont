# -*- coding: utf-8 -*-

from json import load

from .helpers import _add
from .helpers import _assert_symbol_size
from .helpers import _get_tokenizer
from .helpers import _parse_info
from .helpers import _proc_tok
from .utils import pwrite


class Gridfont():
  def __init__(self, fn):
    print('loading:', fn)
    self._load(fn)

  def _load(self, fn):
    with open(fn) as f:
      jsn = load(f)
      self.move = jsn['abs_move']
      self.down = jsn['pen_down']

      # note: these structures are manipulated in place
      self.jsn = jsn
      self.groups = jsn['groups']
      self.symbols = jsn['symbols']
      self.compass = jsn['compass']
      self.all_commands = ''

      # path definition tokenizer
      self.tokfx = _get_tokenizer(self.compass, [self.move, self.down])
    return self

  def _parse_path(self, path):
    state = (0, 0, False)
    # _assert_valid_cmds(self.all_commands)
    for tok in self.tokfx(path):
      cmd, arg = _proc_tok(tok)
      if cmd == self.move:
        state = arg[0], arg[1], state[-1]
      elif cmd == self.down:
        state = state[0], state[1], True
      elif cmd in self.compass:
        npx, npy = _add(state, self.compass[cmd], arg)
        state = npx, npy, state[-1]
      else:
        # this probably wont happen since invalid commands will be ignored by
        # the tokenizer
        raise ValueError('invalid command: {:s}'.format(tok))
      # TODO: what happens if cmd == D? should we add to state the first time
      # always?
      x, y, pen = state
      if pen:
        yield x, y

  def _parse_paths(self, paths):
    for path in paths:
      yield list(self._parse_path(path))

  def parse(self):
    print('parsing ...')
    for char, o in self.symbols.items():
      try:
        info, raw_paths = o['raw'].strip().split(':')
        print('char: {:s} {:s}'.format(char, raw_paths))
        path_strings = list([r.strip() for r in raw_paths.strip().split('|')])
        assert path_strings, 'must have at least one path'
        w, h = _parse_info(info)
        paths = list(self._parse_paths(path_strings))
        assert paths, 'failed to parse at least one path'
        _assert_symbol_size(w, h, paths)
        o['w'] = w
        o['h'] = h
        num = len(paths)
        o['paths'] = paths
        o['num'] = num
        print('      w {:d} h {:d} # {:d}'.format(w, h, num))
      except Exception as e:
        print('error char: {:s} --- {:s}'.format(char, str(e)))
    return self

  def save(self, fn):
    print('writing:', fn)
    with open(fn, 'w') as f:
      pwrite(self.symbols, f)
    return self

