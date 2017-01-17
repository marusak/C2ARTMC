"""Parser of source C code.

Parse the whole file and return writable structure of ARTMC instructions.
"""

from src.tokens import TokenEnum, TokenGroups
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
        t = self.s.get_token()
        while (t != TokenEnum.XEOF):
            if (t == TokenEnum.KWStruct):
                self.parse_struct()
            elif (t == TokenEnum.KWTypedef):
                self.parse_typedef()
            elif (t in TokenGroups.DataTypes):
                pass
            else:
                src.error.FatalError("Unknown construction on line {0}."
                                     .format(self.s.get_current_line()))
            t = self.s.get_token()

    def get_artmc(self):
        """Return converted ARTMC instructions."""
        return self.instructions

    def parse_struct(self):
        """Parse one structure."""
        pass

    def parse_typedef(self):
        """Parse one typedef."""
        pass
