import os

directory, file = os.path.split(__file__)
directory = os.path.expanduser(directory)
directory = os.path.abspath(directory)

sys.path.append(directory)

import pwnfox
