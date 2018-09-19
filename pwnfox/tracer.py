import gdb

from .utils import *
from .constants import *

array_objects = []
objects = []

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

def setup():
  NewArrayBreakpoint()
  NewObjectBreakpoint()
