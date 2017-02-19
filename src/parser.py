"""Parser of source C code.

Parse the whole file and return writable structure of ARTMC instructions.
"""

from src.tokens import TokenEnum, TokenGroups
from src.scanner import Scanner
from src.error import FatalError


class Parser:
    """The parser."""

    def __init__(self, file_name, generate):
        """The init."""
        self.s = Scanner(file_name)
        self.g = generate

        # The name of the structure
        self.structure_name = ""

        # counter to provide unique numbers or labels
        self.unique_counter = 0

        # counter to provide unique numbers or variables
        self.unique_counter_v = 0

    def generate_unique_label_name(self):
        """Return string that is unique."""
        self.unique_counter += 1
        return "label-{0}".format(str(self.unique_counter - 1))

    def generate_unique_variable(self):
        """Create new unique variable."""
        self.unique_counter_v += 1
        name = "v{0}".format(str(self.unique_counter_v - 1))
        self.g.save_new_variable(name)
        return name

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
                self.g.add_pointer_to_structure(next_pointer)
            # data
            elif (token in TokenGroups.DataTypes):
                # parse data element
                self.verify_token(TokenEnum.TIden)
                data = self.s.get_value()
                self.verify_token(TokenEnum.TS)
                self.g.add_data_to_structure(data)
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
        self.g.save_new_variable(self.s.get_value())

        t = self.s.get_token()

        while (t != TokenEnum.TS):
            self.verify_token(TokenEnum.TIden)
            name = self.s.get_value()
            self.g.save_new_variable(name)
            t = self.s.get_token()

            if (t == TokenEnum.TAss):
                t = self.parse_assignment(name)

    def parse_subexpression(self,
                            succ_label,
                            fail_label):
        """Parse subexpression.

        suc_label: label to jump if the expression is successful
        fail_label: label to jump if the expression is unsuccessful
        """
        t = self.s.get_token()

        # ! means negation - switch labels
        if (t == TokenEnum.TN):
            (succ_label, fail_label) = (fail_label, succ_label)
            t = self.s.get_token()

        if (t == TokenEnum.TIden):
            x = self.s.get_value()
            t = self.s.get_token()

            if (t == TokenEnum.TP):
                self.verify_token(TokenEnum.TIden)
                tmp = self.generate_unique_variable()
                self.g.new_i_x_ass_y_next(tmp, x, self.s.get_value())
                x = tmp
                t = self.s.get_token()

            # only support == and !=
            if (t not in [TokenEnum.TE, TokenEnum.TNE]):
                FatalError("Unsupported operator on line {0}"
                           .format(self.s.get_current_line()))
            if (t == TokenEnum.TNE):
                (succ_label, fail_label) = (fail_label, succ_label)

            t = self.s.get_token()

            # x == NULL
            if (t == TokenEnum.KWNull):
                self.g.new_i_x_eq_null(x, succ_label, fail_label)

            # x = y
            elif (t == TokenEnum.TIden):
                y = self.s.get_value()

                t = self.s.get_token()
                if (t != TokenEnum.TP):
                    self.g.new_i_x_eq_y(x, y, succ_label, fail_label)
                    self.s.unget_token(t)

                else:
                    self.verify_token(TokenEnum.TIden)
                    tmp = self.generate_unique_variable()
                    self.g.new_i_x_ass_y_next(tmp, y, self.s.get_value())
                    self.g.new_i_x_eq_y(x, tmp, succ_label, fail_label)

            else:
                FatalError("Unsupported operand on line {0}"
                           .format(self.s.get_current_line()))

        elif (t == TokenEnum.TLZ):
            self.parse_expression(succ_label, fail_label)

        else:
            FatalError("Unknown type in expression on line {0}."
                       .format(self.s.get_current_line()))

    def parse_expression(self,
                         succ_label,
                         fail_label):
        """Parse a expression.

        suc_label: label to jump if the expression is successful
        fail_label: label to jump if the expression is unsuccessful
        """
        # keeping last binary operator
        last_op = None
        # keeping label for repeating binary operator
        until = None

        while (True):
            local_succ = self.generate_unique_label_name()
            local_fail = self.generate_unique_label_name()
            self.parse_subexpression(local_succ, local_fail)

            t = self.s.get_token()

            # )
            if (t == TokenEnum.TPZ):
                if (last_op):
                    # last operator was &&
                    if (last_op == TokenEnum.TAnd):
                        self.g.label_alias(until, fail_label)

                    # last operator was ||
                    else:
                        self.g.label_alias(until, succ_label)

                self.g.label_alias(local_succ, succ_label)
                self.g.label_alias(local_fail, fail_label)
                return

            # &&
            elif (t == TokenEnum.TAnd):
                # case 1 -> first and
                if not last_op:
                    last_op = t
                    until = self.generate_unique_label_name()

                    self.g.label_alias(local_succ, 'next_line')
                    self.g.label_alias(local_fail, until)

                # case 2 -> repeating and
                elif (last_op == t):
                    self.g.label_alias(local_succ, 'next_line')
                    self.g.label_alias(local_fail, until)

                # case 3 -> switching to and from or
                else:
                    self.g.new_label(until)
                    last_op = t
                    until = self.generate_unique_label_name()
                    self.g.label_alias(local_succ, 'next_line')
                    self.g.label_alias(local_fail, until)

            # ||
            elif (t == TokenEnum.TOr):
                # case 1 -> first or
                if not last_op:
                    last_op = t
                    until = self.generate_unique_label_name()
                    self.g.label_alias(local_succ, until)
                    self.g.label_alias(local_fail, 'next_line')

                # case 2 -> repeating or
                elif (last_op == t):
                    self.g.label_alias(local_succ, until)
                    self.g.label_alias(local_fail, 'next_line')

                # case 3 -> switching to or from and
                else:
                    self.g.new_label(until)
                    last_op = t
                    until = self.generate_unique_label_name()
                    self.g.label_alias(local_succ, until)
                    self.g.label_alias(local_fail, 'next_line')

            else:
                FatalError("Unknown token in expression on line {0}."
                           .format(self.s.get_current_line()))

    def parse_while(self):
        """Parse a while statement."""
        succ = self.generate_unique_label_name()
        fail = self.generate_unique_label_name()
        beginning = self.generate_unique_label_name()

        self.g.new_label(beginning)

        self.verify_token(TokenEnum.TLZ)
        self.parse_expression(succ, fail)
        self.g.new_label(succ)

        t = self.s.get_token()
        # { a new block starts
        if (t == TokenEnum.TLZZ):
            t = self.s.get_token()
            while (t != TokenEnum.TPZZ):
                self.parse_command(t)
                t = self.s.get_token()
        else:
            self.parse_command(t)
        self.g.new_i_goto(beginning)
        self.g.new_label(fail)

    def parse_do(self):
        """Parse a do-while statement."""
        succ = self.generate_unique_label_name()
        fail = self.generate_unique_label_name()

        self.g.new_label(succ)

        t = self.s.get_token()
        # { a new block starts
        if (t == TokenEnum.TLZZ):
            t = self.s.get_token()
            while (t != TokenEnum.TPZZ):
                self.parse_command(t)
                t = self.s.get_token()
        else:
            self.parse_command(t)

        self.verify_token(TokenEnum.KWWhile)
        self.verify_token(TokenEnum.TLZ)
        self.parse_expression(succ, fail)

        self.g.new_label(fail)

    def parse_if(self):
        """Parse a if statement."""
        # generate unique labels
        succ = self.generate_unique_label_name()
        fail = self.generate_unique_label_name()
        end = self.generate_unique_label_name()

        self.verify_token(TokenEnum.TLZ)
        self.parse_expression(succ, fail)
        self.g.new_label(succ)
        t = self.s.get_token()
        # { a new block starts
        if (t == TokenEnum.TLZZ):
            t = self.s.get_token()
            while (t != TokenEnum.TPZZ):
                self.parse_command(t)
                t = self.s.get_token()
        else:
            self.parse_command(t)
        self.g.new_i_goto(end)
        self.g.new_label(fail)

        # try a else branch
        t = self.s.get_token()
        if (t != TokenEnum.KWElse):
            self.s.unget_token(t)
        else:
            t = self.s.get_token()
            if (t == TokenEnum.TLZZ):
                t = self.s.get_token()
                while (t != TokenEnum.TPZZ):
                    self.parse_command(t)
                    t = self.s.get_token()
            else:
                self.parse_command(t)

        self.g.new_label(end)

    def parse_return(self):
        """Parse a return statement."""
        self.skip_until_semicolon()
        self.g.new_i_goto("exit")

    def parse_assignment(self, name=None):
        """Parse a variable assignment.

        If 'name' was not passed, name is is self.s.get_value().
        When 'name' was passed, it must be direct assignment name = ...,
        otherwise it can be x->y = ... .

        After this command ',' or ';' may follow. It must return this symbol.
        """
        if (name is None):
            name = self.s.get_value()
            t = self.s.get_token()
            if (t == TokenEnum.TP):
                if (name not in self.g.get_variables()):
                    FatalError("Accessing item of invalid var on line {0}."
                               .format(self.s.get_current_line()))

                self.verify_token(TokenEnum.TIden)
                pointer = self.s.get_value()

                self.verify_token(TokenEnum.TAss)
                t = self.s.get_token()
                # x.next = NULL
                if (t == TokenEnum.KWNull):
                    self.g.new_i_x_next_ass_null(name, pointer)

                # x.next = y
                elif (t == TokenEnum.TIden):
                    self.g.new_i_x_next_ass_y(name,
                                              pointer,
                                              self.s.get_value())

                # x.next = malloc(..);
                elif (t == TokenEnum.KWMalloc):
                    self.skip_until_semicolon()
                    self.g.new_i_x_next_new(name, pointer)

                else:
                    FatalError("Unknown assignment on line {0}"
                               .format(self.s.get_current_line()))
                return

        # skip assignment to variables of different types
        if (name not in self.g.get_variables()):
            self.skip_until_semicolon()
            return TokenEnum.TS

        # command beginning with 'x ='
        t = self.s.get_token()
        # x = null
        if (t == TokenEnum.KWNull):
            self.g.new_i_x_ass_null(name)
            return self.s.get_token()

        # x = y
        elif (t == TokenEnum.TIden):
            second_var = self.s.get_value()
            if (second_var not in self.g.get_variables()):
                FatalError("Unknown variable '{0}' on line {1}."
                           .format(second_var, self.s.get_current_line()))

            t = self.s.get_token()
            if (t in [TokenEnum.TS, TokenEnum.TC]):
                self.g.new_i_x_ass_y(name, second_var)
                return t

            # x = y->next
            elif (t == TokenEnum.TP):
                self.verify_token(TokenEnum.TIden)
                self.g.new_i_x_ass_y_next(name, second_var, self.s.get_value())
                return self.s.get_token()

        else:
            FatalError("Unknown assignment on line {0}"
                       .format(self.s.get_current_line()))

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
                self.g.save_new_variable(self.s.get_value())

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
        while (t != TokenEnum.TPZZ):
            self.parse_command(t)
            t = self.s.get_token()

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
                    self.g.save_new_variable(name)
                    while (t != TokenEnum.TS):
                        self.verify_token(TokenEnum.TIden)
                        name = self.s.get_value()
                        self.g.save_new_variable(name)
                        t = self.s.get_token()

                        if (t == TokenEnum.TAss):
                            t = self.parse_assignment(name)

                # a function
                elif (t == TokenEnum.TLZ):
                    self.parse_function()
                    break

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
