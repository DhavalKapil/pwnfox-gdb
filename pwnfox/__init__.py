from . import jsval
from . import parser

# Setting up tracer
from . import tracer

tracer.setup()

# Setting up commands

from . import commands

commands.setup()
