import os
import sys

print(os.path.dirname(sys.modules['__main__'].__file__))
