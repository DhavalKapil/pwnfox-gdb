from . import *

import gdb
import binascii

MAX_LEN_TO_DISPLAY = 0x10

# Helper functions
def u8(s):
  assert(len(s) == 1)
  return int(binascii.hexlify(s[::-1]), 16)

def u16(s):
  assert(len(s) == 2)
  return int(binascii.hexlify(s[::-1]), 16)

def u32(s):
  assert(len(s) == 4)
  return int(binascii.hexlify(s[::-1]), 16)

def u64(s):
  assert(len(s) == 8)
  return int(binascii.hexlify(s[::-1]), 16)

SIZE_TO_UNPACKER = {
  8: u8,
  16: u16,
  32: u32,
  64: u64
}

def memview_substr(memview, start, end):
  # TODO: Somehow, it only works byte by byte
  # Otherwise throws this error:
  # <class 'BufferError'> memoryview: underlying buffer is not C-contiguous
  content = b""
  for i in range(start, end):
    content += memview[i]
  return content

def arg_to_int(str):
  if str.startswith('0x'):
    return int(str, 16)
  return int(str)

def shape_object(addr):
  inferior = gdb.selected_inferior()

  # Reeading Shape
  shape_contents = inferior.read_memory(addr, 0x20)

  shape = {}
  shape['base_'] = u64(memview_substr(shape_contents, 0, 8))
  shape['propid_'] = u64(memview_substr(shape_contents, 8, 16))
  shape['slotInfo'] = u32(memview_substr(shape_contents, 16, 20))
  shape['attr'] = u8(memview_substr(shape_contents, 20, 21))
  shape['flags'] = u8(memview_substr(shape_contents, 21, 22))
  shape['parent'] = u64(memview_substr(shape_contents, 24, 32))

  return shape

def object_properties(obj):
  inferior = gdb.selected_inferior()

  properties = {}

  # Reading object properties
  shape_addr = obj['shape_']
  while True:
    shape = shape_object(shape_addr)
    if shape['parent'] == 0:
      break

    # Try reading property name, if not treat as integer index
    try:
      prop_name = inferior.read_memory(shape['propid_'] + 8, 0x10).tobytes()
    except:
      prop_name = shape['propid_']

    log.info(prop_name)
    # Getting value
    value_addr = obj['slots_'] + shape['slotInfo']*8
    value = inferior.read_memory(value_addr, 0x8).tobytes()
    log.info(value)

    properties[prop_name] = value

    # Reading next property-value pair
    shape_addr = shape['parent']

  return properties

def native_object(addr):
  inferior = gdb.selected_inferior()

  # Reading NativeObject
  js_object_header = inferior.read_memory(addr, 0x20).tobytes()
  obj = {}
  obj['group_'] = u64(js_object_header[0:8])
  obj['shape_'] = u64(js_object_header[8:16])
  obj['slots_'] = u64(js_object_header[16:24])
  obj['elements_'] = u64(js_object_header[24:32])

  return obj

def array_object(addr):
  inferior = gdb.selected_inferior()

  # Reading ArrayObject
  array = native_object(addr)

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
  len_to_display = obj_elements['length']
  if len_to_display > MAX_LEN_TO_DISPLAY:
    len_to_display = MAX_LEN_TO_DISPLAY

  array_contents = inferior.read_memory(
    array['elements_'],
    8 * len_to_display
  ).tobytes()
  array_content = []
  for i in range(len_to_display):
    array_content.append(array_contents[i*8:i*8+8])
  array['elements_contents'] = array_content

  return array

def typed_array_object(addr, size):
  inferior = gdb.selected_inferior()

  # Reading NativeObject
  typed_array_object = native_object(addr)

  # Reading SLOT metadata
  slot_contents = inferior.read_memory(
    addr + 0x20,
    0x20
  ).tobytes()

  typed_array_object['BUFFER_SLOT'] = jsval.jsval_to_object(
    u64(slot_contents[0:8])
  )
  typed_array_object['LENGTH_SLOT'] = jsval.jsval_to_int32(
    u64(slot_contents[8:16])
  )
  typed_array_object['BYTEOFFSET_SLOT'] = jsval.jsval_to_int32(
    u64(slot_contents[16:24])
  )
  # RESERVED_SLOT is actually the DATA slot
  typed_array_object['RESERVED_SLOT'] = u64(slot_contents[24:32])

  # Reading contents
  len_to_display = typed_array_object['LENGTH_SLOT']
  if len_to_display > MAX_LEN_TO_DISPLAY:
    len_to_display = MAX_LEN_TO_DISPLAY

  array_elements = inferior.read_memory(
    typed_array_object['RESERVED_SLOT'],
    size * len_to_display
  ).tobytes()

  typed_array_object['elements_contents'] = []

  unpack = SIZE_TO_UNPACKER[size]
  for i in range(len_to_display):
    start_index = i*int(size/8)
    end_index = (i+1)*int(size/8)
    typed_array_object['elements_contents'].append(
      unpack(array_elements[start_index:end_index])
    )

  return typed_array_object

def array_buffer_object(addr):
  inferior = gdb.selected_inferior()

  # Reading NativeObject
  array_buffer_object = native_object(addr)

  # Reading SLOT meta data
  slot_contents = inferior.read_memory(
    addr + 0x20,
    0x20
  ).tobytes()

  # Stored pointer is 'private'
  array_buffer_object['DATA_SLOT'] = u64(slot_contents[0:8]) << 1
  array_buffer_object['BYTE_LENGTH_SLOT'] = jsval.jsval_to_int32(
    u64(slot_contents[8:16])
  )
  array_buffer_object['FIRST_VIEW_SLOT'] = jsval.jsval_to_object(
    u64(slot_contents[16:24])
  )
  array_buffer_object['FLAGS_SLOT'] = jsval.jsval_to_int32(
    u64(slot_contents[24:32])
  )

  return array_buffer_object
