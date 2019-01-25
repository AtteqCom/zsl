"""
This script is to specify an appropriate module working with Python 3 (python3_gearman) or Python 2 (gearman).
"""

try:
    import python3_gearman as gearman
except ImportError:
    import gearman
