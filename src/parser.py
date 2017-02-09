"""Parser of source C code.

Parse the whole file and return writable structure of ARTMC instructions.
"""

from src.tokens import TokenEnum, TokenGroups
from src.scanner import Scanner
from src.error import FatalError


class Parser:
    """The parser."""

    def __init__(self, file_name):
        """The init."""
        self.s = Scanner(file_name)
        self.instructions = []
        # All items of the main data structure
        self.structure_pointers = {}
        self.structure_data = {}
        # A counter of items in structure
        self.pointer_counter = 0
        # The name of the structure
        self.structure_name = ""

    def verify_token(self, expected_token):
        """Read next token and compare with expected token."""
        if (self.s.get_token() != expected_token):
            FatalError("Unexpected token on line {0}."
                       .format(self.s.get_current_line()))

    def verify_identifier(self, expected_identifier):
        """Read next token, expect identifier and compare with expected."""
        if (self.s.get_token() != TokenEnum.TIden):
            FatalError("Unexpected identifier on line {0}."
                       .format(self.s.get_current_line()))

        if (self.s.get_value() != expected_identifier):
            FatalError("Unexpected identifier '{0}' on line {1}."
                       .format(expected_identifier,
                               self.s.get_current_line()))

    def add_pointer_to_structure(self, pointer_name):
        """Add new pointer into structure and generate it's unique ID."""
        if (pointer_name in self.structure_pointers.keys()):
            FatalError("Duplicity identifier on line {0}."
                       .format(self.s.get_current_line()))
        # Save new item
        self.structure_pointers[pointer_name] = self.pointer_counter
        self.pointer_counter += 1

    def add_data_to_structure(self, data_name):
        """Add new data item into structure and generate it's unique ID."""
        if (data_name in self.structure_data.keys()):
            FatalError("Duplicity identifier on line {0}."
                       .format(self.s.get_current_line()))
        # Save new item
        self.structure_data[data_name] = self.pointer_counter
        self.pointer_counter += 1

    def parse_typedef(self):
        """Parse one typedef."""
        self.verify_token(TokenEnum.KWStruct)
        self.verify_token(TokenEnum.TIden)
        struct_name = self.s.get_value()
        self.verify_token(TokenEnum.TLZZ)
        token = self.s.get_token()

        while (token != TokenEnum.TPZZ):
            # next pointer
            if (token == TokenEnum.KWStruct):
                self.verify_identifier(struct_name)
                self.verify_token(TokenEnum.TMul)
                self.verify_token(TokenEnum.TIden)
                next_pointer = self.s.get_value()
                self.verify_token(TokenEnum.TS)
                self.add_pointer_to_structure(next_pointer)
            # data
            elif (token in TokenGroups.DataTypes):
                # parse data element
                self.verify_token(TokenEnum.TIden)
                data = self.s.get_value()
                self.verify_token(TokenEnum.TS)
                self.add_data_to_structure(data)
            else:
                FatalError("Unknown item in structure on line {0}."
                           .format(self.s.get_current_line()))

            token = self.s.get_token()

        self.verify_token(TokenEnum.TMul)
        self.verify_token(TokenEnum.TIden)
        self.structure_name = self.s.get_value()
        self.verify_token(TokenEnum.TS)

    def get_output_structure_info(self):
        """Return string to be written into header of program.py."""
        output = "# next pointers are : "
        output += ", ".join('{0}={1}'
                            .format(key, val)
                            for key, val in self.structure_pointers.items())
        output += "\n# data values are : "
        output += ", ".join('{0}={1}'
                            .format(key, val)
                            for key, val in self.structure_data.items())
        return output

    def get_artmc(self):
        """Return converted ARTMC instructions."""
        return self.instructions

    def run(self):
        """Parse the file and convert to ARTMC instructions."""
        t = self.s.get_token()
        while (t != TokenEnum.XEOF):
            if (t == TokenEnum.KWTypedef):
                self.parse_typedef()
            elif (t in TokenGroups.DataTypes):
                pass
            else:
                FatalError("Unknown construction on line {0}."
                           .format(self.s.get_current_line()))
            t = self.s.get_token()
