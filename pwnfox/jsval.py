import struct

# Constants defined in Spidermonkey
JSVAL_TYPE_DOUBLE = 0x00
JSVAL_TYPE_INT32 = 0x01
JSVAL_TYPE_UNDEFINED = 0x02
JSVAL_TYPE_BOOLEAN = 0x03
JSVAL_TYPE_MAGIC = 0x04
JSVAL_TYPE_STRING = 0x05
JSVAL_TYPE_SYMBOL = 0x06
JSVAL_TYPE_PRIVATE_GCTHING = 0x07
JSVAL_TYPE_NULL = 0x08
JSVAL_TYPE_OBJECT = 0x0c

JSVAL_TAG_MAX_DOUBLE = 0x1FFF0
JSVAL_TAG_INT32 = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_INT32
JSVAL_TAG_UNDEFINED = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_UNDEFINED
JSVAL_TAG_STRING = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_STRING
#JSVAL_TAG_SYMBOL = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_SYMBOL
JSVAL_TAG_BOOLEAN = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_BOOLEAN
#JSVAL_TAG_MAGIC = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_MAGIC
JSVAL_TAG_NULL = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_NULL
JSVAL_TAG_OBJECT = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_OBJECT
JSVAL_TAG_PRIVATE_GCTHING = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_PRIVATE_GCTHING

JSVAL_TAG_NULL = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_BOOLEAN
JSVAL_TAG_BOOLEAN = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_MAGIC
JSVAL_TAG_STRING = JSVAL_TAG_MAX_DOUBLE | JSVAL_TYPE_SYMBOL

TAG_STR_MAP = {
  JSVAL_TAG_INT32: "INT32",
  JSVAL_TAG_UNDEFINED: "UNDEFINED",
  JSVAL_TAG_STRING: "STRING",
  JSVAL_TAG_BOOLEAN: "BOOLEAN",
  JSVAL_TAG_NULL: "NULL",
  JSVAL_TAG_OBJECT: "OBJECT",
  JSVAL_TAG_PRIVATE_GCTHING: "PRIVATE_GCTHING"
}

def get_tag(jsval):
  return jsval >> 47

def jsval_to_int32(jsval):
  tag = get_tag(jsval)
  assert(tag == JSVAL_TAG_INT32)
  return jsval & ~(tag << 47)

def jsval_to_object(jsval):
  tag = get_tag(jsval)
  assert(tag == JSVAL_TAG_OBJECT)
  return jsval & ~(tag << 47)

def jsval_to_double(jsval):
  bytes = struct.pack("L", jsval)
  return struct.unpack("d", bytes)[0]

def parse_jsval(jsval):
  val = {}
  tag = get_tag(jsval)
  if tag in TAG_STR_MAP.keys():
    val["TYPE"] = TAG_STR_MAP[tag]
    val["VALUE"] = jsval & ~(tag << 47)
  else:
    val["TYPE"] = "FLOAT"
    val["VALUE"] = jsval_to_double(jsval)
  return val
