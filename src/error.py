"""Modul for processing errors."""

import sys


def fatal_error(msg):
    """Print error and exit."""
    print("Fatal Error: {0}".format(msg))
    sys.exit(1)


def warning(msg):
    """Print warning."""
    print("Warning: {0}".format(msg))
