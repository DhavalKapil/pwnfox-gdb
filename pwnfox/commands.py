import gdb

from . import tracer
from .utils import *

class JSArrayObjectsCommand(gdb.Command):
  "js_array_objects - Displays all javascript array objects"

  def __init__(self):
    super(JSArrayObjectsCommand, self).__init__(
      "js_array_objects",
      gdb.COMMAND_STATUS,
    )

  def invoke(self, argument, from_tty):
    for array_object in tracer.array_objects:
      array = parser.array_object(array_object)
      s = hex(array_object) + ': [ '
      for el in array['content']:
        s += str(el) + ','
      s = s[:-1] + ' ]'
      log.info(s)

class JSArrayObjectCommand(gdb.Command):
  "js_array_object [address] - Parse and display array at this address"

  def __init__(self):
    super(JSArrayObjectCommand, self).__init__(
      "js_array_object",
      gdb.COMMAND_STATUS,
      gdb.COMPLETE_LOCATION,
      False
    )

  def invoke(self, argument, from_tty):
    if argument is None or argument == "":
      log.info("js_array_object requires an address as argument")
      return
    array_addr = parser.arg_to_int(argument)
    arr = parser.array_object(array_addr)
    log.info(arr)

def setup():
  JSArrayObjectsCommand()
  JSArrayObjectCommand()
