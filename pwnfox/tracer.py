import gdb

from pwnfox.utils import *

array_objects = []

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

def setup():
  NewArrayBreakpoint()
