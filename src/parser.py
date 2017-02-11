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

        # All items of the main data structure and it's instances
        self.structure_pointers = {}
        self.structure_data = {}
        self.variables = {}

        # A counter of unique ids
        self.pointer_counter = 0
        self.variables_counter = 0

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

    def save_new_variable(self, variable_name):
        """Add new variable and generate it's unique ID."""
        if (variable_name in self.variables.keys()):
            FatalError("Duplicity variable on line {0}."
                       .format(self.s.get_current_line()))
        # Save new item
        self.variables[variable_name] = self.variables_counter
        self.variables_counter += 1

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

    def skip_until_semicolon(self):
        """Read and ignore all tokens until semicolon."""
        t = self.s.get_token()
        while (t != TokenEnum.TS):
            t = self.s.get_token()

    def parse_new_definition_of_structure(self):
        """Parse line on which definition(s) or declaration(s) are.

        Expects that the variables are of the structure type.
        """
        self.verify_token(TokenEnum.TIden)
        self.save_new_variable(self.s.get_value())

        t = self.s.get_token()

        while (t != TokenEnum.TS):
            self.verify_token(TokenEnum.TIden)
            self.save_new_variable(self.s.get_value())
            t = self.s.get_token()
        # TODO may be a definition as well

    def parse_while(self):
        """Parse a while statement."""
        pass
        # TODO

    def parse_for(self):
        """Parse a for statement."""
        pass
        # TODO

    def parse_do(self):
        """Parse a do-while statement."""
        pass
        # TODO

    def parse_if(self):
        """Parse a if statement."""
        pass
        # TODO

    def parse_return(self):
        """Parse a return statement."""
        pass
        # TODO

    def parse_assignment(self):
        """Parse a variable assignment."""
        pass
        # TODO
        # x = ...
        # x->next = ...
        # x = ... and x is not a structure type variable

    def parse_command(self, first_token):
        """Parse one single command."""
        # definition/declaration of the structure type
        if (first_token == TokenEnum.TIden and
           self.s.get_value() == self.structure_name):
            self.parse_new_definition_of_structure()

        # definition/declaration of the standard types
        elif (first_token in TokenGroups.DataTypes):
            # ignore this variables
            self.skip_until_semicolon()

        # a while statement
        elif (first_token == TokenEnum.KWWhile):
            self.parse_while()

        # a for statement
        elif (first_token == TokenEnum.KWFor):
            self.parse_for()

        # a do-while statement
        elif (first_token == TokenEnum.KWDo):
            self.parse_do()

        # a if statement
        elif (first_token == TokenEnum.KWIf):
            self.parse_if()

        # a return statement
        elif (first_token == TokenEnum.KWReturn):
            self.parse_return()

        # a variable assignment
        elif (first_token == TokenEnum.TIden):
            self.parse_assignment()

    def parse_function(self):
        """Parse function. It is already read for the first '('."""
        t = self.s.get_token()

        # parse function arguments
        while (t != TokenEnum.TPZ):
            # argument of the main structure
            if (t == TokenEnum.TIden and
               self.s.get_value() == self.structure_name):
                self.verify_token(TokenEnum.TIden)
                self.save_new_variable(self.s.get_value())

            # argument of other types
            elif (t in TokenGroups.DataTypes):
                self.verify_token(TokenEnum.TIden)

            else:
                FatalError("Unknown argument type on line {0}."
                           .format(self.s.get_current_line()))

            t = self.s.get_token()
            if (t == TokenEnum.TC):
                t = self.s.get_token()

        self.verify_token(TokenEnum.TLZZ)

        t = self.s.get_token()
        while (t != TokenEnum.TPZ):
            self.parse_command(t)
            t = self.s.get_token()

    def get_output_structure_info(self):
        """Return string to be written into header of program.py."""
        output = "# pointer variables are : "
        output += ", ".join('{0}={1}'
                            .format(key, val)
                            for key, val in self.variables.items())
        output += "\n# next pointers are : "
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
            # a typedef
            if (t == TokenEnum.KWTypedef):
                self.parse_typedef()

            # a function on variable of the main strucutre
            elif (t == TokenEnum.TIden and
                  self.s.get_value() == self.structure_name):
                self.verify_token(TokenEnum.TIden)
                name = self.s.get_value()
                t = self.s.get_token()

                # variable declaration(s)
                if (t in [TokenEnum.TC, TokenEnum.TS]):
                    self.save_new_variable(name)
                    while (t != TokenEnum.TS):
                        self.verify_token(TokenEnum.TIden)
                        self.save_new_variable(self.s.get_value())
                        t = self.s.get_token()

                    # TODO may be a definition as well

                # a function
                elif (t == TokenEnum.TLZ):
                    self.parse_function()

                else:
                    FatalError("Unsupported construction on line {0}."
                               .format(self.s.get_current_line()))

            # a function
            elif (t in TokenGroups.DataTypes):
                self.verify_token(TokenEnum.TIden)
                name = self.s.get_value()
                self.verify_token(TokenEnum.TLZ)
                self.parse_function()

            else:
                FatalError("Unknown construction on line {0}."
                           .format(self.s.get_current_line()))
            t = self.s.get_token()
