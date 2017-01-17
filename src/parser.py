"""Parser of source C code.

Parse the whole file and return writable structure of ARTMC instructions.
"""

from src.tokens import TokenEnum, TokenType
from src.scanner import Scanner
import src.error


class Parser:
    """The parser."""

    def __init__(self, file_name):
        """The init."""
        self.s = Scanner(file_name)
        self.instructions = []

    def run(self):
        """Parse the file and convert to ARTMC instructions."""
        pass

    def get_artmc(self):
        """Return converted ARTMC instructions."""
        return self.instructions
