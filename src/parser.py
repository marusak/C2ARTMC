"""Parser of source C code.

Parse the whole file and return writable structure of ARTMC instructions.
"""

from src.tokens import TokenEnum, TokenGroups
from src.scanner import Scanner
from src.error import fatal_error, warning

# there is never too-many ;)
# pylint: disable=R0911,R0912,R0915,R0904,R0902


class Parser:
    """The parser."""

    def __init__(self, file_name, generate, ignore):
        """The init."""
        self.scanner = Scanner(file_name)
        self.gen = generate

        # The name of the structure
        self.structure_name = ""

        # counter to provide unique numbers or labels
        self.unique_counters = [0, 0]

        self.ignore = ignore

        self.last_begining = []
        self.last_end = []
        self.unique_variables = []
        self.unique_context = 0

    def generate_unique_label_name(self):
        """Return string that is unique."""
        self.unique_counters[0] += 1
        return "label-{0}".format(str(self.unique_counters[0] - 1))

    def generate_unique_variable(self):
        """Create new unique variable."""
        if len(self.unique_variables) > self.unique_context:
            self.unique_context += 1
            return self.unique_variables[self.unique_context - 1]

        self.unique_counters[1] += 1
        name = "v{0}".format(str(self.unique_counters[1] - 1))
        self.gen.save_new_variable(name)
        self.unique_variables.append(name)
        self.unique_context += 1
        return name

    def restart_unique_context(self):
        """Restart unique context - tmp variables can be reused."""
        self.unique_context = 0

    def verify_token(self, expected_token, err_message=None):
        """Read next token and compare with expected token."""
        if self.scanner.get_token() != expected_token:
            if err_message:
                fatal_error(err_message)
            else:
                fatal_error("Unexpected token on line {0}."
                            .format(self.scanner.get_current_line()))

    def verify_identifier(self, expected_identifier):
        """Read next token, expect identifier and compare with expected."""
        if self.scanner.get_token() != TokenEnum.TIden:
            fatal_error("Unexpected identifier on line {0}."
                        .format(self.scanner.get_current_line()))

        if self.scanner.get_value() != expected_identifier:
            fatal_error("Unexpected identifier '{0}' on line {1}."
                        .format(expected_identifier,
                                self.scanner.get_current_line()))

    def parse_typedef(self):
        """Parse one typedef."""
        self.verify_token(TokenEnum.KWStruct)
        self.verify_token(TokenEnum.TIden)
        struct_name = self.scanner.get_value()
        self.verify_token(TokenEnum.TLZZ)
        token = self.scanner.get_token()

        while token != TokenEnum.TPZZ:
            # next pointer
            if token == TokenEnum.KWStruct:
                self.verify_identifier(struct_name)
                self.verify_token(TokenEnum.TMul)
                self.verify_token(TokenEnum.TIden)
                next_pointer = self.scanner.get_value()
                self.verify_token(TokenEnum.TS)
                current_line = self.scanner.get_current_line()
                self.gen.add_pointer_to_structure(next_pointer,
                                                  current_line)
            # data
            elif token in TokenGroups.DataTypes:
                # parse data element
                self.verify_token(TokenEnum.TIden)
                data = self.scanner.get_value()
                self.verify_token(TokenEnum.TS)
                self.gen.add_data_to_structure(data,
                                               self.scanner.get_current_line())
            else:
                fatal_error("Unknown item in structure on line {0}."
                            .format(self.scanner.get_current_line()))

            token = self.scanner.get_token()

        self.verify_token(TokenEnum.TMul)
        self.verify_token(TokenEnum.TIden)
        self.structure_name = self.scanner.get_value()
        self.verify_token(TokenEnum.TS)

    def skip_until_semicolon(self):
        """Read and ignore all tokens until semicolon."""
        token = self.scanner.get_token()
        while token != TokenEnum.TS:
            token = self.scanner.get_token()

    def skip_subexpression(self):
        """Read and ignore all tokens creating subexpression."""
        token = self.scanner.get_token()
        while (token not in [TokenEnum.TPZ, TokenEnum.TAnd, TokenEnum.TOr]):
            token = self.scanner.get_token()
        self.scanner.unget_token(token)

    def parse_struct_definition(self):
        """Parse line on which definition(s) or declaration(s) are.

        Expects that the variables are of the structure type.
        """
        self.verify_token(TokenEnum.TIden)
        self.gen.save_new_variable(self.scanner.get_value())

        token = self.scanner.get_token()
        if token == TokenEnum.TAss:
            token = self.parse_assignment(self.scanner.get_value())
            self.restart_unique_context()

        while token != TokenEnum.TS:
            self.verify_token(TokenEnum.TIden)
            name = self.scanner.get_value()
            self.gen.save_new_variable(name)
            token = self.scanner.get_token()

            if token == TokenEnum.TAss:
                token = self.parse_assignment(name)
                self.restart_unique_context()

    def parse_subexpression(self,
                            succ_label,
                            fail_label,
                            abstr):
        """Parse subexpression.

        suc_label: label to jump if the expression is successful
        fail_label: label to jump if the expression is unsuccessful
        abstr: if true, first command does not include NO_ABSTR
        """
        processing_data = False
        token = self.scanner.get_token()

        # ! means negation - switch labels
        if token == TokenEnum.TN:
            (succ_label, fail_label) = (fail_label, succ_label)
            token = self.scanner.get_token()

        if token == TokenEnum.TIden:
            xname = self.scanner.get_value()
            token = self.scanner.get_token()

            while token == TokenEnum.TP:
                self.verify_token(TokenEnum.TIden)
                pointer = self.scanner.get_value()

                # it may be just comparing data
                if pointer == self.gen.get_data_name():
                    processing_data = True
                    token = self.scanner.get_token()
                    break
                else:
                    tmp = self.generate_unique_variable()
                    self.gen.new_i_x_ass_y_next(tmp, xname, pointer, abstr)
                    abstr = False
                    xname = tmp

                token = self.scanner.get_token()

            # using short comparing e.g if(x) or if(x->data) etc.
            if (token in [TokenEnum.TPZ, TokenEnum.TOr, TokenEnum.TAnd]):
                if processing_data:
                    if self.ignore:
                        self.gen.new_i_if_star(succ_label, fail_label, abstr)
                        abstr = False
                    else:
                        self.gen.new_i_ifdata(xname,
                                              0,
                                              fail_label,
                                              succ_label,
                                              abstr)
                        abstr = False
                else:
                    self.gen.new_i_x_eq_null(xname,
                                             fail_label,
                                             succ_label,
                                             abstr)
                    abstr = False

                self.scanner.unget_token(token)
                return

            # only support == and !=
            if processing_data and token in TokenGroups.DataComparators:
                if self.ignore:
                    self.gen.new_i_if_star(succ_label, fail_label, abstr)
                    abstr = False
                    self.skip_subexpression()
                    return
                else:
                    fatal_error(("Unsupported comparing on line {0}. "
                                 "Comparing data can only be == or !=. "
                                 "Try -i to ignore.")
                                .format(self.scanner.get_current_line()))

            if token not in [TokenEnum.TE, TokenEnum.TNE]:
                fatal_error("Unsupported operator on line {0}"
                            .format(self.scanner.get_current_line()))
            if token == TokenEnum.TNE:
                (succ_label, fail_label) = (fail_label, succ_label)

            token = self.scanner.get_token()

            # x == NULL
            if token == TokenEnum.KWNull:
                self.gen.new_i_x_eq_null(xname, succ_label, fail_label, abstr)
                abstr = False

            # x = y
            elif token == TokenEnum.TIden:
                yname = self.scanner.get_value()

                if processing_data:
                    if self.ignore:
                        self.gen.new_i_if_star(succ_label, fail_label, abstr)
                        abstr = False
                    else:
                        value = self.gen.get_standard_val(yname)
                        self.gen.new_i_ifdata(xname,
                                              value,
                                              succ_label,
                                              fail_label,
                                              abstr)
                        abstr = False
                    return

                token = self.scanner.get_token()
                while token == TokenEnum.TP:
                    self.verify_token(TokenEnum.TIden)
                    tmp = self.generate_unique_variable()
                    self.gen.new_i_x_ass_y_next(tmp,
                                                yname,
                                                self.scanner.get_value(),
                                                abstr)
                    abstr = False
                    yname = tmp
                    token = self.scanner.get_token()

                self.gen.new_i_x_eq_y(xname,
                                      yname,
                                      succ_label,
                                      fail_label,
                                      abstr)
                abstr = False
                self.scanner.unget_token(token)

            elif token in TokenGroups.Datas and processing_data:
                if self.ignore:
                    self.gen.new_i_if_star(succ_label, fail_label, abstr)
                    abstr = False
                else:
                    self.gen.new_i_ifdata(xname,
                                          self.scanner.get_value(),
                                          succ_label,
                                          fail_label,
                                          abstr)
                    abstr = False

            else:
                fatal_error("Unsupported operand on line {0}"
                            .format(self.scanner.get_current_line()))

        elif token == TokenEnum.TLZ:
            self.parse_expression(succ_label, fail_label)

        elif token in TokenGroups.Nondeterministic:
            self.gen.new_i_if_star(succ_label, fail_label, abstr)
            abstr = False

        elif token == TokenEnum.KWTrue:
            self.gen.new_i_goto(succ_label, abstr)
            abstr = False

        elif token == TokenEnum.KWFalse:
            self.gen.new_i_goto(fail_label, abstr)
            abstr = False

        else:
            fatal_error("Unknown type in expression on line {0}."
                        .format(self.scanner.get_current_line()))

    def parse_expression(self,
                         succ_label,
                         fail_label,
                         abstr=False):
        """Parse a expression.

        suc_label: label to jump if the expression is successful
        fail_label: label to jump if the expression is unsuccessful
        no_abstr: if true, first command does not include NO_ABSTR
        """
        # keeping last binary operator
        last_op = None
        # keeping label for repeating binary operator
        until = None

        while True:
            local_succ = self.generate_unique_label_name()
            local_fail = self.generate_unique_label_name()
            self.parse_subexpression(local_succ, local_fail, abstr)
            abstr = False
            self.restart_unique_context()

            token = self.scanner.get_token()

            # )
            if token == TokenEnum.TPZ:
                if last_op:
                    # last operator was &&
                    if last_op == TokenEnum.TAnd:
                        self.gen.label_alias(until, fail_label)

                    # last operator was ||
                    else:
                        self.gen.label_alias(until, succ_label)

                self.gen.label_alias(local_succ, succ_label)
                self.gen.label_alias(local_fail, fail_label)
                return

            # &&
            elif token == TokenEnum.TAnd:
                # case 1 -> first and
                if not last_op:
                    last_op = token
                    until = self.generate_unique_label_name()

                    self.gen.label_alias(local_succ, 'next_line')
                    self.gen.label_alias(local_fail, until)

                # case 2 -> repeating and
                elif last_op == token:
                    self.gen.label_alias(local_succ, 'next_line')
                    self.gen.label_alias(local_fail, until)

                # case 3 -> switching to and from or
                else:
                    self.gen.new_label(until)
                    last_op = token
                    until = self.generate_unique_label_name()
                    self.gen.label_alias(local_succ, 'next_line')
                    self.gen.label_alias(local_fail, until)

            # ||
            elif token == TokenEnum.TOr:
                # case 1 -> first or
                if not last_op:
                    last_op = token
                    until = self.generate_unique_label_name()
                    self.gen.label_alias(local_succ, until)
                    self.gen.label_alias(local_fail, 'next_line')

                # case 2 -> repeating or
                elif last_op == token:
                    self.gen.label_alias(local_succ, until)
                    self.gen.label_alias(local_fail, 'next_line')

                # case 3 -> switching to or from and
                else:
                    self.gen.new_label(until)
                    last_op = token
                    until = self.generate_unique_label_name()
                    self.gen.label_alias(local_succ, until)
                    self.gen.label_alias(local_fail, 'next_line')

            else:
                fatal_error("Unknown token in expression on line {0}."
                            .format(self.scanner.get_current_line()))

    def parse_while(self):
        """Parse a while statement."""
        succ = self.generate_unique_label_name()
        fail = self.generate_unique_label_name()
        beginning = self.generate_unique_label_name()

        self.last_begining.append(beginning)
        self.last_end.append(fail)

        self.gen.new_label(beginning)

        self.verify_token(TokenEnum.TLZ)
        self.parse_expression(succ, fail, True)
        self.gen.new_label(succ)

        token = self.scanner.get_token()
        # { a new block starts
        if token == TokenEnum.TLZZ:
            token = self.scanner.get_token()
            while token != TokenEnum.TPZZ:
                self.parse_command(token)
                token = self.scanner.get_token()
        else:
            self.parse_command(token)
        self.gen.new_i_goto(beginning)
        self.gen.new_label(fail)
        self.last_begining.pop()
        self.last_end.pop()

    def parse_do(self):
        """Parse a do-while statement."""
        succ = self.generate_unique_label_name()
        fail = self.generate_unique_label_name()
        beginning = self.generate_unique_label_name()

        self.gen.new_label(succ)
        self.last_begining.append(beginning)
        self.last_end.append(fail)

        token = self.scanner.get_token()
        # { a new block starts
        if token == TokenEnum.TLZZ:
            token = self.scanner.get_token()
            while token != TokenEnum.TPZZ:
                self.parse_command(token)
                token = self.scanner.get_token()
        else:
            self.parse_command(token)

        self.verify_token(TokenEnum.KWWhile)
        self.verify_token(TokenEnum.TLZ)

        self.gen.new_label(beginning)

        self.parse_expression(succ, fail, True)

        self.gen.new_label(fail)
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
        self.gen.new_label(succ)
        token = self.scanner.get_token()
        # { a new block starts
        if token == TokenEnum.TLZZ:
            token = self.scanner.get_token()
            while token != TokenEnum.TPZZ:
                self.parse_command(token)
                token = self.scanner.get_token()
        else:
            self.parse_command(token)
        self.gen.new_i_goto(end)
        self.gen.new_label(fail)

        # try a else branch
        token = self.scanner.get_token()
        if token != TokenEnum.KWElse:
            self.scanner.unget_token(token)
        else:
            token = self.scanner.get_token()
            if token == TokenEnum.TLZZ:
                token = self.scanner.get_token()
                while token != TokenEnum.TPZZ:
                    self.parse_command(token)
                    token = self.scanner.get_token()
            else:
                self.parse_command(token)

        self.gen.new_label(end)

    def parse_return(self):
        """Parse a return statement."""
        token = self.scanner.get_token()
        if token == TokenEnum.KWError:
            self.skip_until_semicolon()
            self.gen.new_i_error()
        else:
            self.scanner.unget_token(token)
            self.skip_until_semicolon()
            self.gen.new_i_goto("exit")

    def parse_goto(self):
        """Parse a goto statement."""
        self.verify_token(TokenEnum.TIden)
        self.gen.new_i_goto("custom_" + self.scanner.get_value())
        self.verify_token(TokenEnum.TS)

    def parse_assert(self):
        """Parse a assert statement."""
        succ = self.generate_unique_label_name()
        fail = self.generate_unique_label_name()

        self.verify_token(TokenEnum.TLZ)
        self.parse_expression(succ, fail)
        self.gen.new_label(fail)
        self.gen.new_i_error()
        self.gen.new_label(succ)
        self.verify_token(TokenEnum.TS)

    def parse_assignment(self, name=None):
        """Parse a variable assignment.

        If 'name' was not passed, name is is self.scanner.get_value().
        When 'name' was passed, it must be direct assignment name = ...,
        otherwise it can be x->y = ... .

        After this command ',' or ';' may follow. It must return this symbol.
        """
        if name is None:
            name = self.scanner.get_value()
            token = self.scanner.get_token()
            if token == TokenEnum.TP:
                if name not in self.gen.get_variables():
                    fatal_error("Accessing item of invalid var on line {0}."
                                .format(self.scanner.get_current_line()))

                self.verify_token(TokenEnum.TIden)
                pointer = self.scanner.get_value()

                token = self.scanner.get_token()
                while token == TokenEnum.TP:
                    self.verify_token(TokenEnum.TIden)
                    ptr = self.scanner.get_value()
                    tmp = self.generate_unique_variable()
                    self.gen.new_i_x_ass_y_next(tmp,
                                                name,
                                                pointer)
                    name = tmp
                    pointer = ptr
                    token = self.scanner.get_token()

                if token in TokenGroups.DataOperators:
                    if self.ignore:
                        self.skip_until_semicolon()
                        return TokenEnum.TS
                    else:
                        fatal_error(("Data manipulation is not supported on "
                                     "line {0}. Try -i for ignoring data.")
                                    .format(self.scanner.get_current_line()))

                if token != TokenEnum.TAss:
                    fatal_error("Unknown token in assignment on line {0}."
                                .format(self.scanner.get_current_line()))

                token = self.scanner.get_token()

                # x.next = NULL
                if token == TokenEnum.KWNull:
                    self.gen.new_i_x_next_ass_null(name, pointer)

                # x.next = y
                elif token == TokenEnum.TIden:
                    if pointer == self.gen.get_data_name():
                        if not self.ignore:
                            current_line = self.scanner.get_current_line()
                            yname = self.scanner.get_value()
                            value = self.gen.get_standard_val(yname)
                            self.gen.new_i_setdata(name,
                                                   pointer,
                                                   value,
                                                   current_line)
                    else:
                        yname = self.scanner.get_value()
                        token = self.scanner.get_token()

                        while token == TokenEnum.TP:
                            self.verify_token(TokenEnum.TIden)
                            ptr = self.scanner.get_value()
                            tmp = self.generate_unique_variable()
                            self.gen.new_i_x_ass_y_next(tmp,
                                                        yname,
                                                        ptr)
                            yname = tmp
                            token = self.scanner.get_token()

                        self.scanner.unget_token(token)
                        self.gen.new_i_x_next_ass_y(name, pointer, yname)

                # x.next = malloc(..);
                elif token == TokenEnum.KWMalloc:
                    self.skip_until_semicolon()
                    self.gen.new_i_x_next_new(name, pointer)
                    return TokenEnum.TS

                elif token in TokenGroups.Datas:
                    if not self.ignore:
                        self.gen.new_i_setdata(name,
                                               pointer,
                                               self.scanner.get_value(),
                                               self.scanner.get_current_line())

                else:
                    fatal_error("Unknown assignment on line {0}"
                                .format(self.scanner.get_current_line()))
                return self.scanner.get_token()

            elif token == TokenEnum.TCO:
                self.gen.new_label("custom_" + name)

        # skip assignment to variables of different types
        if name not in self.gen.get_variables():
            if name in self.gen.get_constants():
                if not self.ignore:
                    # try simple value change, e.g. x = 5; x = 7;
                    token = self.scanner.get_token()
                    cur_v = self.scanner.get_value()
                    if token in TokenGroups.Datas:
                        self.gen.add_standard_variable(name, cur_v)
                    elif token == TokenEnum.TIden:
                        new_v = self.gen.get_standard_val(cur_v)
                        self.gen.add_standard_variable(name, new_v)
                    else:
                        fatal_error(("Only simple changing of values on "
                                     "standard variables is allowed on line "
                                     "{0}. Try -i to ignore.")
                                    .format(self.scanner.get_current_line()))
                    self.verify_token(TokenEnum.TS,
                                      ("Only simple changing of values on "
                                       "standard variables is allowed on line "
                                       "{0}. Try -i to ignore.")
                                      .format(self.scanner.get_current_line()))
                else:
                    warning("Skipping command beginning with '{0}' on line {1}"
                            .format(name, self.scanner.get_current_line()))
                    self.skip_until_semicolon()
            else:
                warning("Skipping 2 command beginning with '{0}' on line {1}."
                        .format(name, self.scanner.get_current_line()))
                self.skip_until_semicolon()
            return TokenEnum.TS

        # command beginning with 'x ='
        token = self.scanner.get_token()
        # x = null
        if token == TokenEnum.KWNull:
            self.gen.new_i_x_ass_null(name)
            return self.scanner.get_token()

        # x = y
        elif token == TokenEnum.TIden:
            second_var = self.scanner.get_value()
            if second_var not in self.gen.get_variables():
                fatal_error("Unknown variable '{0}' on line {1}."
                            .format(second_var,
                                    self.scanner.get_current_line()))

            token = self.scanner.get_token()
            if (token in [TokenEnum.TS, TokenEnum.TC]):
                self.gen.new_i_x_ass_y(name, second_var)
                return token

            # x = y->next->next...
            elif token == TokenEnum.TP:
                self.verify_token(TokenEnum.TIden)
                pointer = self.scanner.get_value()

                token = self.scanner.get_token()
                while token == TokenEnum.TP:
                    self.verify_token(TokenEnum.TIden)
                    ptr = self.scanner.get_value()
                    tmp = self.generate_unique_variable()
                    self.gen.new_i_x_ass_y_next(tmp,
                                                second_var,
                                                pointer)
                    second_var = tmp
                    pointer = ptr
                    token = self.scanner.get_token()

                self.gen.new_i_x_ass_y_next(name, second_var, pointer)
                return token

        elif token == TokenEnum.KWMalloc:
            self.skip_until_semicolon()
            self.gen.new_i_new(name)
            return TokenEnum.TS

        elif token == TokenEnum.KWRandomAlloc:
            self.skip_until_semicolon()
            self.gen.new_i_random_alloc(name)
            return TokenEnum.TS

        else:
            fatal_error("Unknown assignment on line {0}"
                        .format(self.scanner.get_current_line()))

    def parse_command(self, first_token):
        """Parse one single command."""
        # definition/declaration of the structure type
        if (first_token == TokenEnum.TIden and
                self.scanner.get_value() == self.structure_name):
            self.parse_struct_definition()

        # definition/declaration of the standard types
        elif first_token in TokenGroups.DataTypes:
            self.verify_token(TokenEnum.TIden)
            name = self.scanner.get_value()
            token = self.scanner.get_token()
            if token == TokenEnum.TS:
                self.gen.add_standard_variable(name, 0)
            elif token == TokenEnum.TAss:
                token = self.scanner.get_token()
                if token in TokenGroups.Datas:
                    self.gen.add_standard_variable(name,
                                                   self.scanner.get_value())
                elif token == TokenEnum.TIden:
                    new_v = self.gen.get_standard_val(self.scanner.get_value())
                    self.gen.add_standard_variable(name, new_v)
                else:
                    fatal_error("Unsupported editing of value on line {0}"
                                .format(self.scanner.get_current_line()))
                if self.scanner.get_token() != TokenEnum.TS:
                    fatal_error("Unsupported editing of value on line {0}"
                                .format(self.scanner.get_current_line()))
            else:
                fatal_error("Unsupported editing of value on line {0}"
                            .format(self.scanner.get_current_line()))

        # a while statement
        elif first_token == TokenEnum.KWWhile:
            self.parse_while()

        # a do-while statement
        elif first_token == TokenEnum.KWDo:
            self.parse_do()

        # a if statement
        elif first_token == TokenEnum.KWIf:
            self.parse_if()

        # a return statement
        elif first_token == TokenEnum.KWReturn:
            self.parse_return()

        # a variable assignment
        elif first_token == TokenEnum.TIden:
            self.parse_assignment()
            self.restart_unique_context()

        # a break statement
        elif first_token == TokenEnum.KWBreak:
            self.gen.new_i_goto(self.last_end[-1])
            self.verify_token(TokenEnum.TS)

        # a continue statement
        elif first_token == TokenEnum.KWContinue:
            self.gen.new_i_goto(self.last_begining[-1])
            self.verify_token(TokenEnum.TS)

        elif first_token == TokenEnum.KWAssert:
            self.parse_assert()

        elif first_token == TokenEnum.KWGoto:
            self.parse_goto()

    def parse_function(self):
        """Parse function. It is already read for the first '('."""
        token = self.scanner.get_token()

        # parse function arguments
        while token != TokenEnum.TPZ:
            # argument of the main structure
            if (token == TokenEnum.TIden and
                    self.scanner.get_value() == self.structure_name):
                self.verify_token(TokenEnum.TIden)
                self.gen.save_new_variable(self.scanner.get_value())

            # argument of other types
            elif token in TokenGroups.DataTypes:
                self.verify_token(TokenEnum.TIden)
                self.gen.add_standard_variable(self.scanner.get_value(), 0)

            else:
                fatal_error("Unknown argument type on line {0}."
                            .format(self.scanner.get_current_line()))

            token = self.scanner.get_token()
            if token == TokenEnum.TC:
                token = self.scanner.get_token()

        self.verify_token(TokenEnum.TLZZ)

        token = self.scanner.get_token()
        while token != TokenEnum.TPZZ:
            self.parse_command(token)
            token = self.scanner.get_token()

    def run(self):
        """Parse the file and convert to ARTMC instructions."""
        token = self.scanner.get_token()
        function_read = False
        while token != TokenEnum.XEOF:
            # a typedef
            if token == TokenEnum.KWTypedef:
                self.parse_typedef()

            # a function on variable of the main strucutre
            elif (token == TokenEnum.TIden and
                  self.scanner.get_value() == self.structure_name or
                  token in TokenGroups.DataTypes):

                standard = True if token in TokenGroups.DataTypes else False

                self.verify_token(TokenEnum.TIden)
                name = self.scanner.get_value()
                token = self.scanner.get_token()

                # variable declaration(s)
                if (token in [TokenEnum.TC, TokenEnum.TS]):
                    if standard:
                        self.gen.add_standard_variable(name, 0)
                    else:
                        self.gen.save_new_variable(name)
                    while token != TokenEnum.TS:
                        self.verify_token(TokenEnum.TIden)
                        name = self.scanner.get_value()
                        if standard:
                            self.gen.add_standard_variable(name, 0)
                        else:
                            self.gen.save_new_variable(name)
                        token = self.scanner.get_token()

                        if token == TokenEnum.TAss:
                            token = self.parse_assignment(name)
                            self.restart_unique_context()

                # a function
                elif token == TokenEnum.TLZ:
                    if function_read:
                        fatal_error(("There is more than one function."
                                     "Only the first one is parsed."))
                    self.parse_function()
                    function_read = True

                else:
                    fatal_error("Unsupported construction on line {0}."
                                .format(self.scanner.get_current_line()))

            else:
                fatal_error("Unknown construction on line {0}."
                            .format(self.scanner.get_current_line()))
            token = self.scanner.get_token()
