import sys

def debug(s):
  sys.stdout.write("[*] DEBUG: ")
  print(s)

def error(s):
  sys.stdout.write("[*] ERROR: ")
  print(s)

def info(s):
  sys.stdout.write("[*] INFO: ")
  print(s)
