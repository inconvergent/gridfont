# -*- coding: utf-8 -*-

from json import dumps
from json import dump
from traceback import print_exc


def pprint(jsn):
  print(dumps(jsn, indent=2, sort_keys=True))
  return jsn

def pwrite(jsn, f):
  dump(jsn, f, indent=2, sort_keys=True)
  return jsn

def show_exception():
  return print_exc()

