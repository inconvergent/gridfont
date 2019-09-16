# -*- coding: utf-8 -*-

def _add(a, b, s):
  return a[0] + s*b[0], a[1] + s*b[1]

def _alter_state(state, cmd, s=1):
  a, b = _add(state, cmd, s)
  if len(cmd) < 3:
    return a, b, state[2]
  return a, b, cmd[2]


def _parse_size(s):
  assert s.startswith('S'), 'must start with "S"'
  w, h = [int(i) for i in s[1:].split(',')]
  return w, h

def _next_cmd_ind(compass, p, _from):
  n = len(p)
  for i in range(_from+1, n):
    if p[i] in compass:
      return i
  return n


def _parse_path(compass, p):
  state = (0, 0, False)
  n = len(p)
  i = 0
  path = []
  while i < n:
    c = p[i]
    next_ind = _next_cmd_ind(compass, p, i)
    scale = int(p[i+1:next_ind]) if (next_ind-i) > 1 else 1
    cmd = compass[c]
    state = _alter_state(state, cmd, scale)
    x, y, pen = state
    if pen:
      path.append((x, y))
    i = next_ind
  return path

def _parse_paths(compass, pp):
  for p in pp:
    yield _parse_path(compass, p)

