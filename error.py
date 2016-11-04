"""Modul for processing errors."""

import sys


def FatalError(msg):
    """Print error and exit."""
    print ("Fatal Error: {0}".format(msg))
    sys.exit(1)


def Warning(msg):
    """Print warning."""
    print ("Warning: {0}".format(msg))
