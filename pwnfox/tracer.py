import gdb

from .utils import *
from .constants import *

array_objects = []
objects = []

uint8_array_objects = []
int8_array_objects = []
uint16_array_objects = []
int16_array_objects = []
uint32_array_objects = []
int32_array_objects = []

class NewArrayFinishBreakpoint(gdb.FinishBreakpoint):
  def __init__(self):
    gdb.FinishBreakpoint.__init__(
      self,
      gdb.newest_frame(),
      internal = True
    )
    self.silent = True

  def stop(self):
    log.debug("NewArray finished")
    frame = gdb.newest_frame()
    arr_addr = int(frame.read_register('rax'))
    array_objects.append(arr_addr)
    return False

class NewArrayBreakpoint(gdb.Breakpoint):
  def __init__(self):
    gdb.Breakpoint.__init__(
      self,
      'NewArray<4294967295u>',
      internal = True
    )
    self.silent = True

  def stop(self):
    log.debug("NewArray called")
    NewArrayFinishBreakpoint()
    return False

# NewObject isn't a direct correlation with SpiderMonkey's NewObject.
# It is mainly for explicit objects like: obj = {a: "b"};
class NewObjectFinishBreakpoint(gdb.FinishBreakpoint):
  def __init__(self):
    gdb.FinishBreakpoint.__init__(
      self,
      gdb.newest_frame(),
      internal = True
    )
    self.silent = True

  def stop(self):
    log.debug("NewObject finished")
    frame = gdb.newest_frame()
    obj_addr = int(frame.read_register('rax'))
    objects.append(obj_addr)
    return False

class NewObjectBreakpoint(gdb.Breakpoint):
  def __init__(self):
    gdb.Breakpoint.__init__(
      self,
      'NewObject',
      internal = True
    )
    self.silent = True

  def stop(self):
    # Verify NewObjectKind (stored in rcx)
    frame = gdb.newest_frame()
    rip = int(frame.read_register('rip'))
    kind = int(frame.read_register('rcx'))
    if kind != JS_SINGLETON_OBJECT:
      return False
    log.debug("Singleton Object")
    NewObjectFinishBreakpoint()
    return False

# Template super classes for TypedArrayObject
class NewTypedArrayObjectFinishBreakpoint(gdb.FinishBreakpoint):
  def __init__(self, array_type, typed_array_objects):
    gdb.FinishBreakpoint.__init__(
      self,
      gdb.newest_frame(),
      internal = True
    )
    self.silent = True
    self.array_type = array_type
    self.typed_array_objects = typed_array_objects

  def stop(self):
    log.debug("NewTypedArrayObject<%s> finished" % self.array_type)
    frame = gdb.newest_frame()
    typed_arr_addr = int(frame.read_register('rax'))
    self.typed_array_objects.append(typed_arr_addr)
    return False

class NewTypedArrayObjectBreakpoint(gdb.Breakpoint):
  def __init__(self, array_type, finish_breakpoint):
    gdb.Breakpoint.__init__(
      self,
      '(anonymous namespace)::TypedArrayObjectTemplate<%s>::makeInstance' % array_type,
      internal = True
    )
    self.silent = True
    self.array_type = array_type
    self.finish_breakpoint = finish_breakpoint

  def stop(self):
    log.debug("NewTypedArrayObject<%s> called" % self.array_type)
    self.finish_breakpoint()
    return False

class NewUint8ArrayFinishBreakpoint(NewTypedArrayObjectFinishBreakpoint):
  def __init__(self):
    NewTypedArrayObjectFinishBreakpoint.__init__(
      self,
      "unsigned char",
      uint8_array_objects
    )

class NewUint8ArrayBreakpoint(NewTypedArrayObjectBreakpoint):
  def __init__(self):
    NewTypedArrayObjectBreakpoint.__init__(
      self,
      "unsigned char",
      NewUint8ArrayFinishBreakpoint
    )

class NewInt8ArrayFinishBreakpoint(NewTypedArrayObjectFinishBreakpoint):
  def __init__(self):
    NewTypedArrayObjectFinishBreakpoint.__init__(
      self,
      "signed char",
      int8_array_objects
    )

class NewInt8ArrayBreakpoint(NewTypedArrayObjectBreakpoint):
  def __init__(self):
    NewTypedArrayObjectBreakpoint.__init__(
      self,
      "signed char",
      NewInt8ArrayFinishBreakpoint
    )

class NewUint16ArrayFinishBreakpoint(NewTypedArrayObjectFinishBreakpoint):
  def __init__(self):
    NewTypedArrayObjectFinishBreakpoint.__init__(
      self,
      "unsigned short",
      uint16_array_objects
    )

class NewUint16ArrayBreakpoint(NewTypedArrayObjectBreakpoint):
  def __init__(self):
    NewTypedArrayObjectBreakpoint.__init__(
      self,
      "unsigned short",
      NewUint16ArrayFinishBreakpoint
    )

class NewInt16ArrayFinishBreakpoint(NewTypedArrayObjectFinishBreakpoint):
  def __init__(self):
    NewTypedArrayObjectFinishBreakpoint.__init__(
      self,
      "signed short",
      int16_array_objects
    )

class NewInt16ArrayBreakpoint(NewTypedArrayObjectBreakpoint):
  def __init__(self):
    NewTypedArrayObjectBreakpoint.__init__(
      self,
      "signed short",
      NewInt16ArrayFinishBreakpoint
    )

class NewUint32ArrayFinishBreakpoint(NewTypedArrayObjectFinishBreakpoint):
  def __init__(self):
    NewTypedArrayObjectFinishBreakpoint.__init__(
      self,
      "unsigned int",
      uint32_array_objects
    )

class NewUint32ArrayBreakpoint(NewTypedArrayObjectBreakpoint):
  def __init__(self):
    NewTypedArrayObjectBreakpoint.__init__(
      self,
      "unsigned int",
      NewUint32ArrayFinishBreakpoint
    )

class NewInt32ArrayFinishBreakpoint(NewTypedArrayObjectFinishBreakpoint):
  def __init__(self):
    NewTypedArrayObjectFinishBreakpoint.__init__(
      self,
      "signed int",
      int32_array_objects
    )

class NewInt32ArrayBreakpoint(NewTypedArrayObjectBreakpoint):
  def __init__(self):
    NewTypedArrayObjectBreakpoint.__init__(
      self,
      "signed int",
      NewInt32ArrayFinishBreakpoint
    )

def setupTypedArrayObjectBreakpoints():
  NewUint8ArrayBreakpoint()
  NewInt8ArrayBreakpoint()
  NewUint16ArrayBreakpoint()
  NewInt16ArrayBreakpoint()
  NewUint32ArrayBreakpoint()
  NewInt32ArrayBreakpoint()

def setup():
  NewArrayBreakpoint()
  NewObjectBreakpoint()

  setupTypedArrayObjectBreakpoints()
