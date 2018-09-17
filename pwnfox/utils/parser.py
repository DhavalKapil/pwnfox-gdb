import gdb
import binascii

# Helper functions
def u32(s):
  assert(len(s) == 4)
  return int(binascii.hexlify(s[::-1]), 16)

def u64(s):
  assert(len(s) == 8)
  return int(binascii.hexlify(s[::-1]), 16)

def arg_to_int(str):
  if str.startswith('0x'):
    return int(str, 16)
  return int(str)

def array_object(addr):
  inferior = gdb.selected_inferior()

  # Reading ArrayObject
  array_object_header = inferior.read_memory(addr, 0x20).tobytes()
  array = {}
  array['group_'] = u64(array_object_header[0:8])
  array['shape_'] = u64(array_object_header[8:16])
  array['slots_'] = u64(array_object_header[16:24])
  array['elements_'] = u64(array_object_header[24:32])

  # Reading ObjectElements
  obj_elements_contents = inferior.read_memory(
    array['elements_'] - 0x10,
    0x10
  ).tobytes()
  obj_elements = {}
  obj_elements['flags'] = u32(obj_elements_contents[0:4])
  obj_elements['initializedLength'] = u32(obj_elements_contents[4:8])
  obj_elements['capacity'] = u32(obj_elements_contents[8:12])
  obj_elements['length'] = u32(obj_elements_contents[12:16])
  array['obj_elements'] = obj_elements

  # Reading Array elements
  array_contents = inferior.read_memory(
    array['elements_'],
    8 * obj_elements['length']
  ).tobytes()
  array_content = []
  for i in range(obj_elements['length']):
    array_content.append(array_contents[i*8:i*8+8])
  array['content'] = array_content

  return array
