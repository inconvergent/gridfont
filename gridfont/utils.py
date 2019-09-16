# -*- coding: utf-8 -*-

from json import dumps
from json import dump


def pprint(jsn):
  print(dumps(jsn, indent=2, sort_keys=True))
  return jsn

def pwrite(jsn, f):
  dump(jsn, f, indent=2, sort_keys=True)
  return jsn

