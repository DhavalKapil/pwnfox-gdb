import gdb

from pwnfox.utils import *

class NewArrayFinishBreakpoint(gdb.FinishBreakpoint):
  def __init__(self):
    gdb.FinishBreakpoint.__init__(
      self,
      gdb.newest_frame(),
      internal = True
    )
    self.silent = True

  def stop(self):
    # TODO: NewArray() returned
    log.debug("NewArray finished")
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
    # TODO: NewArray() has just been called
    log.debug("NewArray called")
    NewArrayFinishBreakpoint()
    return False

def setup():
  NewArrayBreakpoint()
