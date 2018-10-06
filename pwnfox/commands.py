import gdb

from . import *
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
      s = hex(array_object) + \
          ": (%d elements) [ " % array['obj_elements']['length']
      for el in array['elements_contents']:
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

class JSObjectsCommand(gdb.Command):
  "js_objects - Displays all javascript objects"

  def __init__(self):
    super(JSObjectsCommand, self).__init__(
      "js_objects",
      gdb.COMMAND_STATUS,
    )

  def invoke(self, argument, from_tty):
    for js_object in tracer.objects:
      array = parser.native_object(js_object)
      s = hex(js_object)
      log.info(s)

class JSObjectCommand(gdb.Command):
  "js_object [address] - Parse and display object at this address"

  def __init__(self):
    super(JSObjectCommand, self).__init__(
      "js_object",
      gdb.COMMAND_STATUS,
      gdb.COMPLETE_LOCATION,
      False
    )

  def invoke(self, argument, from_tty):
    if argument is None or argument == "":
      log.info("js_object requires an address as argument")
      return
    obj_addr = parser.arg_to_int(argument)
    obj = parser.native_object(obj_addr)
    properties = parser.object_properties(obj)
    log.info(obj)
    log.info(properties)

class JSTypedArrayObjectsCommand(gdb.Command):
  def __init__(self, name, typed_array_objects, size):
    super(JSTypedArrayObjectsCommand, self).__init__(
      name,
      gdb.COMMAND_STATUS,
    )
    self.name = name
    self.typed_array_objects = typed_array_objects
    self.size = size

  def invoke(self, argument, from_tty):
    for typed_array_object in self.typed_array_objects:
      array = parser.typed_array_object(typed_array_object, self.size)
      s = hex(typed_array_object) + \
          ": (%d elements) " % array['LENGTH_SLOT']
      log.info(s)

class JSUint8ArraysCommand(JSTypedArrayObjectsCommand):
  "js_uint8_arrays - Displays all javascript uint8 arrays"
  def __init__(self):
    super(JSUint8ArraysCommand, self).__init__(
      "js_uint8_arrays",
      tracer.uint8_array_objects,
      8
    )
    print(parser)

class JSInt8ArraysCommand(JSTypedArrayObjectsCommand):
  "js_int8_arrays - Displays all javascript int8 arrays"
  def __init__(self):
    super(JSInt8ArraysCommand, self).__init__(
      "js_int8_arrays",
      tracer.int8_array_objects,
      8
    )

class JSUint16ArraysCommand(JSTypedArrayObjectsCommand):
  "js_uint16_arrays - Displays all javascript uint16 arrays"
  def __init__(self):
    super(JSUint16ArraysCommand, self).__init__(
      "js_uint16_arrays",
      tracer.uint16_array_objects,
      16
    )

class JSInt16ArraysCommand(JSTypedArrayObjectsCommand):
  "js_int16_arrays - Displays all javascript int16 arrays"
  def __init__(self):
    super(JSInt16ArraysCommand, self).__init__(
      "js_int16_arrays",
      tracer.int16_array_objects,
      16
    )

class JSUint32ArraysCommand(JSTypedArrayObjectsCommand):
  "js_uint32_arrays - Displays all javascript uint32 arrays"
  def __init__(self):
    super(JSUint32ArraysCommand, self).__init__(
      "js_uint32_arrays",
      tracer.uint32_array_objects,
      32
    )

class JSInt32ArraysCommand(JSTypedArrayObjectsCommand):
  "js_int32_arrays - Displays all javascript int32 arrays"
  def __init__(self):
    super(JSInt32ArraysCommand, self).__init__(
      "js_int32_arrays",
      tracer.int32_array_objects,
      32
    )

class JSTypedArrayObjectCommand(gdb.Command):
  def __init__(self, name, size):
    super(JSTypedArrayObjectCommand, self).__init__(
      name,
      gdb.COMMAND_STATUS,
      gdb.COMPLETE_LOCATION,
      False
    )
    self.name = name
    self.size = size

  def invoke(self, argument, from_tty):
    print(argument)
    if argument is None or argument == "":
      log.info("%s requires an address as argument" % self.name)
      return
    array_addr = parser.arg_to_int(argument)
    arr = parser.typed_array_object(array_addr, self.size)
    log.info(arr)

class JSUint8ArrayCommand(JSTypedArrayObjectCommand):
  "js_uint8_array [address] - Parse and display the uint8 array at address"
  def __init__(self):
    super(JSUint8ArrayCommand, self).__init__(
      "js_uint8_array",
      8
    )

class JSInt8ArrayCommand(JSTypedArrayObjectCommand):
  "js_int8_array [address] - Parse and display the int8 array at address"
  def __init__(self):
    super(JSInt8ArrayCommand, self).__init__(
      "js_int8_array",
      8
    )

class JSUint16ArrayCommand(JSTypedArrayObjectCommand):
  "js_uint16_array [address] - Parse and display the uint16 array at address"
  def __init__(self):
    super(JSUint16ArrayCommand, self).__init__(
      "js_uint16_array",
      16
    )

class JSInt16ArrayCommand(JSTypedArrayObjectCommand):
  "js_int16_array [address] - Parse and display the int16 array at address"
  def __init__(self):
    super(JSInt16ArrayCommand, self).__init__(
      "js_int16_array",
      16
    )

class JSUint32ArrayCommand(JSTypedArrayObjectCommand):
  "js_uint32_array [address] - Parse and display the uint32 array at address"
  def __init__(self):
    super(JSUint32ArrayCommand, self).__init__(
      "js_uint32_array",
      32
    )

class JSInt32ArrayCommand(JSTypedArrayObjectCommand):
  "js_int32_array [address] - Parse and display the int32 array at address"
  def __init__(self):
    super(JSInt32ArrayCommand, self).__init__(
      "js_int32_array",
      32
    )

def setupJSTypedArrayCommands():
  JSUint8ArraysCommand()
  JSInt8ArraysCommand()
  JSUint16ArraysCommand()
  JSInt16ArraysCommand()
  JSUint32ArraysCommand()
  JSInt32ArraysCommand()

  JSUint8ArrayCommand()
  JSInt8ArrayCommand()
  JSUint16ArrayCommand()
  JSInt16ArrayCommand()
  JSUint32ArrayCommand()
  JSInt32ArrayCommand()

def setup():
  JSArrayObjectsCommand()
  JSArrayObjectCommand()
  JSObjectsCommand()
  JSObjectCommand()

  setupJSTypedArrayCommands()
