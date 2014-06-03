"""
Settings used by diabetes_problems project.

This consists of the general produciton settings, with an optional import of any local
settings.
"""

# Import production settings.
from diabetes_problems.settings.production import *

# Import optional local settings.
try:
    from diabetes_problems.settings.local import *
except ImportError:
    pass