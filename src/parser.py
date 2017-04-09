"""Parser of source C code.

Parse the whole file and return writable structure of ARTMC instructions.
"""

from src.tokens import TokenEnum, TokenGroups
from src.scanner import Scanner
from src.error import FatalError


class Parser:
    """The parser."""

    def __init__(self, file_name, generate, ignore):
        """The init."""
        self.s = Scanner(file_name)
        self.g = generate

        # The name of the structure
        self.structure_name = ""

        # counter to provide unique numbers or labels
        self.unique_counter = 0

        # counter to provide unique numbers or variables
        self.unique_counter_v = 0

        self.ignore = ignore

        self.last_begining = []
        self.last_end = []

    def generate_unique_label_name(self):
        """Return string that is unique."""
        self.unique_counter += 1
        return "label-{0}".format(str(self.unique_counter - 1))

    def generate_unique_variable(self):
        """Create new unique variable."""
        self.unique_counter_v += 1
        name = "v{0}".format(str(self.unique_counter_v - 1))
        self.g.save_new_variable(name,
                                 self.s.get_current_line())
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
                self.g.add_pointer_to_structure(next_pointer,
                                                self.s.get_current_line())
            # data
            elif (token in TokenGroups.DataTypes):
                # parse data element
                self.verify_token(TokenEnum.TIden)
                data = self.s.get_value()
                self.verify_token(TokenEnum.TS)
                self.g.add_data_to_structure(data,
                                             self.s.get_current_line())
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

    def skip_subexpression(self):
        """Read and ignore all tokens creating subexpression."""
        t = self.s.get_token()
        while (t not in [TokenEnum.TPZ, TokenEnum.TAnd, TokenEnum.TOr]):
            t = self.s.get_token()
        self.s.unget_token(t)

    def parse_new_definition_of_structure(self):
        """Parse line on which definition(s) or declaration(s) are.

        Expects that the variables are of the structure type.
        """
        self.verify_token(TokenEnum.TIden)
        self.g.save_new_variable(self.s.get_value(),
                                 self.s.get_current_line())

        t = self.s.get_token()
        if (t == TokenEnum.TAss):
            t = self.parse_assignment(self.s.get_value())

        while (t != TokenEnum.TS):
            self.verify_token(TokenEnum.TIden)
            name = self.s.get_value()
            self.g.save_new_variable(name, self.s.get_current_line())
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
        processing_data = False
        t = self.s.get_token()

        # ! means negation - switch labels
        if (t == TokenEnum.TN):
            (succ_label, fail_label) = (fail_label, succ_label)
            t = self.s.get_token()

        if (t == TokenEnum.TIden):
            x = self.s.get_value()
            t = self.s.get_token()

            while (t == TokenEnum.TP):
                self.verify_token(TokenEnum.TIden)
                pointer = self.s.get_value()

                # it may be just comparing data
                if (pointer == self.g.get_data_name()):
                    processing_data = True
                    t = self.s.get_token()
                    break
                else:
                    tmp = self.generate_unique_variable()
                    self.g.new_i_x_ass_y_next(tmp, x, pointer)
                    x = tmp

                t = self.s.get_token()

            # using short comparing e.g if(x) or if(x->data) etc.
            if (t in [TokenEnum.TPZ, TokenEnum.TOr, TokenEnum.TAnd]):
                if processing_data:
                    if (self.ignore):
                        self.g.new_i_if_star(succ_label, fail_label)
                    else:
                        self.g.new_i_ifdata(x,
                                            0,
                                            fail_label,
                                            succ_label)
                else:
                    self.g.new_i_x_eq_null(x, fail_label, succ_label)

                self.s.unget_token(t)
                return

            # only support == and !=
            if (processing_data and t in TokenGroups.DataComparators):
                if (self.ignore):
                    self.g.new_i_if_star(succ_label, fail_label)
                    self.skip_subexpression()
                    return
                else:
                    FatalError(("Unsupported comparing on line {0}. Comparing "
                                "data can only be == or !=. Try -i to ignore.")
                               .format(self.s.get_current_line()))

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

                if (processing_data):
                    if (self.ignore):
                        self.g.new_i_if_star(succ_label, fail_label)
                    else:
                        self.g.new_i_ifdata(x,
                                            y,
                                            succ_label,
                                            fail_label)
                    return

                t = self.s.get_token()
                while (t == TokenEnum.TP):
                    self.verify_token(TokenEnum.TIden)
                    tmp = self.generate_unique_variable()
                    self.g.new_i_x_ass_y_next(tmp, y, self.s.get_value())
                    y = tmp
                    t = self.s.get_token()

                self.g.new_i_x_eq_y(x, y, succ_label, fail_label)
                self.s.unget_token(t)

            elif (t in TokenGroups.Datas and processing_data):
                if (self.ignore):
                    self.g.new_i_if_star(succ_label, fail_label)
                else:
                    self.g.new_i_ifdata(x,
                                        self.s.get_value(),
                                        succ_label,
                                        fail_label)

            else:
                FatalError("Unsupported operand on line {0}"
                           .format(self.s.get_current_line()))

        elif (t == TokenEnum.TLZ):
            self.parse_expression(succ_label, fail_label)

        elif (t in TokenGroups.Nondeterministic):
            self.g.new_i_if_star(succ_label, fail_label)

        elif (t == TokenEnum.KWTrue):
            self.g.new_i_goto(succ_label)

        elif (t == TokenEnum.KWFalse):
            self.g.new_i_goto(fail_label)

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

        self.last_begining.append(beginning)
        self.last_end.append(fail)

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
        self.last_begining.pop()
        self.last_end.pop()

    def parse_do(self):
        """Parse a do-while statement."""
        succ = self.generate_unique_label_name()
        fail = self.generate_unique_label_name()
        beginning = self.generate_unique_label_name()

        self.g.new_label(succ)
        self.last_begining.append(beginning)
        self.last_end.append(fail)

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

        self.g.new_label(beginning)

        self.parse_expression(succ, fail)

        self.g.new_label(fail)
        self.last_begining.pop()
        self.last_end.pop()

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
        t = self.s.get_token()
        if (t == TokenEnum.KWError):
            self.skip_until_semicolon()
            self.g.new_i_error()
        else:
            self.s.unget_token(t)
            self.skip_until_semicolon()
            self.g.new_i_goto("exit")

    def parse_goto(self):
        """Parse a goto statement."""
        self.verify_token(TokenEnum.TIden)
        self.g.new_i_goto("custom_" + self.s.get_value())
        self.verify_token(TokenEnum.TS)

    def parse_assert(self):
        """Parse a assert statement."""
        succ = self.generate_unique_label_name()
        fail = self.generate_unique_label_name()

        self.verify_token(TokenEnum.TLZ)
        self.parse_expression(succ, fail)
        self.g.new_label(fail)
        self.g.new_i_error()
        self.g.new_label(succ)
        self.verify_token(TokenEnum.TS)

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

                t = self.s.get_token()
                while (t == TokenEnum.TP):
                    self.verify_token(TokenEnum.TIden)
                    p = self.s.get_value()
                    tmp = self.generate_unique_variable()
                    self.g.new_i_x_ass_y_next(tmp,
                                              name,
                                              pointer)
                    name = tmp
                    pointer = p
                    t = self.s.get_token()

                if (t in TokenGroups.DataOperators):
                    if (self.ignore):
                        self.skip_until_semicolon()
                        return TokenEnum.TS
                    else:
                        FatalError(("Data manipulation is not supported on "
                                   "line {0}. Try -i for ignoring data.")
                                   .format(self.s.get_current_line()))

                if (t != TokenEnum.TAss):
                    FatalError("Unknown token in assignment on line {0}."
                               .format(self.s.get_current_line()))

                t = self.s.get_token()

                # x.next = NULL
                if (t == TokenEnum.KWNull):
                    self.g.new_i_x_next_ass_null(name, pointer)

                # x.next = y
                elif (t == TokenEnum.TIden):
                    if (pointer == self.g.get_data_name()):
                        if (not self.ignore):
                            self.g.new_i_setdata(name,
                                                 pointer,
                                                 self.s.get_value(),
                                                 self.s.get_current_line())
                    else:
                        y = self.s.get_value()
                        t = self.s.get_token()

                        while (t == TokenEnum.TP):
                            self.verify_token(TokenEnum.TIden)
                            p = self.s.get_value()
                            tmp = self.generate_unique_variable()
                            self.g.new_i_x_ass_y_next(tmp,
                                                      y,
                                                      p)
                            y = tmp
                            t = self.s.get_token()

                        self.s.unget_token(t)
                        self.g.new_i_x_next_ass_y(name, pointer, y)

                # x.next = malloc(..);
                elif (t == TokenEnum.KWMalloc):
                    self.skip_until_semicolon()
                    self.g.new_i_x_next_new(name, pointer)
                    return TokenEnum.TS

                elif (t in TokenGroups.Datas):
                    if (not self.ignore):
                        self.g.new_i_setdata(name,
                                             pointer,
                                             self.s.get_value(),
                                             self.s.get_current_line())

                else:
                    FatalError("Unknown assignment on line {0}"
                               .format(self.s.get_current_line()))
                return self.s.get_token()

            elif (t == TokenEnum.TCO):
                self.g.new_label("custom_" + name)

        # skip assignment to variables of different types
        if (name not in self.g.get_variables()):
            if (name in self.g.get_constants() and not self.ignore):
                FatalError("Changing value of standard variable on line {0}.\
                        These operation are not permitted. Use -i to ignore."
                           .format(self.s.get_current_line()))
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

            # x = y->next->next...
            elif (t == TokenEnum.TP):
                self.verify_token(TokenEnum.TIden)
                pointer = self.s.get_value()

                t = self.s.get_token()
                while (t == TokenEnum.TP):
                    self.verify_token(TokenEnum.TIden)
                    p = self.s.get_value()
                    tmp = self.generate_unique_variable()
                    self.g.new_i_x_ass_y_next(tmp,
                                              second_var,
                                              pointer)
                    second_var = tmp
                    pointer = p
                    t = self.s.get_token()

                self.g.new_i_x_ass_y_next(name, second_var, pointer)
                return t

        elif (t == TokenEnum.KWMalloc):
            self.skip_until_semicolon()
            self.g.new_i_new(name)
            return TokenEnum.TS

        elif (t == TokenEnum.KWRandomAlloc):
            self.skip_until_semicolon()
            self.g.new_i_random_alloc(name)
            return TokenEnum.TS

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
            self.verify_token(TokenEnum.TIden)
            self.g.add_standard_variable(self.s.get_value(),
                                         self.s.get_current_line())
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

        # a break statement
        elif (first_token == TokenEnum.KWBreak):
            self.g.new_i_goto(self.last_end[-1])
            self.verify_token(TokenEnum.TS)

        # a continue statement
        elif (first_token == TokenEnum.KWContinue):
            self.g.new_i_goto(self.last_begining[-1])
            self.verify_token(TokenEnum.TS)

        elif (first_token == TokenEnum.KWAssert):
            self.parse_assert()

        elif (first_token == TokenEnum.KWGoto):
            self.parse_goto()

    def parse_function(self):
        """Parse function. It is already read for the first '('."""
        t = self.s.get_token()

        # parse function arguments
        while (t != TokenEnum.TPZ):
            # argument of the main structure
            if (t == TokenEnum.TIden and
               self.s.get_value() == self.structure_name):
                self.verify_token(TokenEnum.TIden)
                self.g.save_new_variable(self.s.get_value(),
                                         self.s.get_current_line())

            # argument of other types
            elif (t in TokenGroups.DataTypes):
                self.verify_token(TokenEnum.TIden)
                self.g.add_standard_variable(self.s.get_value(),
                                             self.s.get_current_line())

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
                  self.s.get_value() == self.structure_name or
                  t in TokenGroups.DataTypes):

                standard = True if t in TokenGroups.DataTypes else False

                self.verify_token(TokenEnum.TIden)
                name = self.s.get_value()
                t = self.s.get_token()

                # variable declaration(s)
                if (t in [TokenEnum.TC, TokenEnum.TS]):
                    if standard:
                        self.g.add_standard_variable(name,
                                                     self.s.get_current_line())
                    else:
                        self.g.save_new_variable(name,
                                                 self.s.get_current_line())
                    while (t != TokenEnum.TS):
                        self.verify_token(TokenEnum.TIden)
                        name = self.s.get_value()
                        line = self.s.get_current_line()
                        if standard:
                            self.g.add_standard_variable(name, line)
                        else:
                            self.g.save_new_variable(name, line)
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

            else:
                FatalError("Unknown construction on line {0}."
                           .format(self.s.get_current_line()))
            t = self.s.get_token()
