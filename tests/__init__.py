# Make tests directory a Python package

# Add src directory to Python path to allow imports
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))