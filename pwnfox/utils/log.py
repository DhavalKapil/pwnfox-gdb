import sys
import inspect
import pprint

pp = pprint.PrettyPrinter(indent=2)

def debug(s):
  sys.stdout.write("[*] DEBUG: ")
  print(s)

def error(s):
  sys.stdout.write("[*] ERROR: ")
  print(s)

def info(s):
  sys.stdout.write("[*] INFO: ")
  pp.pprint(s)

def pprint(obj):
  sys.stdout.write("[*] PPRINT: ")
  for i in inspect.getmembers(obj):
    if not inspect.ismethod(i[1]):
      print(i)
