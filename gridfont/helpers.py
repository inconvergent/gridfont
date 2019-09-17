# -*- coding: utf-8 -*-

from re import compile as re_compile



def _get_all_commands(compass, special):
  cmd = set(compass.keys())
  cmd.update(set(special))
  assert len(compass.keys()) == len(cmd)-len(special),\
      'compass can not contain commands with the same name as commands' +\
      'defined in the special section.'
  return cmd

def _get_tokenizer(cmd):
  r = re_compile(r'[{:s}][0-9,]*'.format(''.join(cmd)))
  return lambda p: [x.group(0) for x in r.finditer(p)]


def _rel_move(a, b, arg=1):
  if isinstance(arg, tuple):
    return a[0] + arg[0]*b[0], a[1] + arg[1]*b[1]
  return a[0] + arg*b[0], a[1] + arg*b[1]

def _parse_info(s):
  assert s.startswith('S'), 'must start with "S"'
  w, h = [int(i) for i in s[1:].strip().split(',')]
  return w, h

def _proc_tok(tok):
  cmd = tok[0]
  arg = tok[1:]
  return cmd, _proc_arg(arg)

def _proc_arg(arg):
  if not arg:
    return 1
  if ',' in arg:
    return tuple([int(a) for a in arg.split(',')])
  return int(arg)


def _assert_symbol_size(w, h, paths):
  for path in paths:
    for x, y in path:
      assert 0 <= x < w, 'x is out of bounds: {:d}'.format(x)
      assert 0 <= y < h, 'y is out of bounds: {:d}'.format(y)
  return True

base_symbols = '0123456789,'
def _assert_valid_cmds(cmd, path):
  for p in path:
    assert p in cmd or p in base_symbols, 'not a valid command: {:s}'.format(p)
  return True

