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
from .utils import show_exception


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

  def _do_cmd(self, start, state, bbox, cmd, arg):
    if cmd == self.special['abs_move']:
      if isinstance(arg, (tuple, list)):
        return arg[0], arg[1], state[-1]
      return arg, arg, state[-1]
    if cmd == self.special['pen_down']:
      return state[0], state[1], True

    # start
    if cmd == self.special['start']:
      return start[0], start[1], state[-1]

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

    raise ValueError('encountered invalid command: {}'.format(cmd))

  def _parse_path(self, bbox, path):
    state = (0, 0, False)
    _assert_valid_cmds(self.all_commands, path)
    res = []
    for tok in self.tokfx(path):
      cmd, arg = _proc_tok(tok)
      state = self._do_cmd(res[0] if res else (0, 0), state, bbox, cmd, arg)
      x, y, pen = state
      if pen:
        res.append((x, y))
    return res

  def _parse_paths(self, bbox, paths):
    for path in paths:
      yield self._parse_path(bbox, path)

  def _parse_path_raw_paths(self, w, h, raw_paths, lenient=False):
    path_strings = list([r.strip() for r in raw_paths.strip().split('|')])
    if len(path_strings) == 1 and not path_strings[0]:
      # empty path definition. this is ok
      return []
    assert path_strings, 'definition must have at least one path'
    paths = list(self._parse_paths((w, h), path_strings))
    for p in paths:
      assert p, 'at least one path is empty, did you forget D?'
    if not lenient:
      _assert_symbol_size(w, h, paths)
    return paths

  def parse(self, lenient=False):
    print('parsing ...')
    for symb, o in self.symbols.items():
      try:
        raw = o['raw']
        raw_split = raw.strip().split(':')
        assert len(raw_split) > 1,\
            'path definition must be on the format info:paths'
        info, raw_paths = raw_split
        w, h = _parse_info(info)
        paths = self._parse_path_raw_paths(w, h, raw_paths, lenient)
        o.update({
            'gw': w, 'gh': h,
            'w': w-1, 'h': h-1,
            'paths': paths,
            'ord': ord(symb),
            'num': len(paths)})
        print('\nsymb: {:s} {:s}'.format(symb, raw))
        print('  --> w {:d} h {:d} # {:d}'.format(w, h, len(paths)))
      except AssertionError as e:
        print('\n!error: {:s} --- {}'.format(symb, e))
      except Exception as e:
        show_exception()
    return self

  def scale(self, s):
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
        print('!svg err on symb: {:s}: {}'.format(symb, e))
        show_exception()
    return self

  def save(self, out):
    fn = out.joinpath('res.json')
    print('writing:', fn)
    with open(str(fn), 'w') as f:
      pwrite(self.symbols, f)
    return self

