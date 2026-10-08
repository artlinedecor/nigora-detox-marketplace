import os
import sys

# Add root folder to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app
