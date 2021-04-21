#!/usr/bin/env python3

# Add path to the ETB module
import sys
# Check the Python version
assert sys.version_info >= (3, 0), "ETB requires Python 3!"
# Add base folder to path
sys.path.insert(1, '../')
# Import the ETB module
from ETB import ETB
