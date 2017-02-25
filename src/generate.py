"""Store instructions and generating output code."""

from src.error import FatalError
from subprocess import Popen, PIPE
from os.path import dirname, abspath, join


class Generate:
    """The class for storing and generating output code."""

    def __init__(self, descriptor=None):
        """The init."""
        self.instructions = []

        # All items of the main data structure and it's instances
        self.structure_pointers = {}
        self.mapped_data = {}
        self.variables = {}
        self.data_name = None

        # A counter of unique ids
        self.pointer_counter = 0
        self.variables_counter = 1

        # A counter of lines
        self.current_line = 0

        # A counter for generating unique data
        self.current_data = 1

        # Dictionary of labels
        self.labels = {'next_line': 'to: next_line'}

        # Aliases of labels
        self.aliases = {}

        # descr_num
        if not descriptor:
            try:
                cmd = Popen([join(dirname(dirname(dirname(abspath(__file__)))),
                             "bin/get_typedef_descr.t.sh")],
                            stdout=PIPE,
                            stderr=PIPE)
                stdout, stderr = cmd.communicate()
            except:
                FatalError("Could not call get_typedef_descr.t.sh. " +
                           "Is the C2ARTMC in the correct place?")

            if (cmd.returncode):
                FatalError("Could not call get_typedef_descr.t.sh." +
                           "Does the current directory contains 'typedef' " +
                           "file? Use -d to set descriptor.")
            self.descr_num = int(stdout) + 1

        else:
            self.descr_num = int(descriptor) + 1

    def get_descr_num(self):
        """Return next descr_num."""
        to_return = self.descr_num
        self.descr_num += 1
        return str(to_return)

    def add_pointer_to_structure(self, pointer_name, current_line):
        """Add new pointer into structure and generate it's unique ID."""
        if (pointer_name in self.structure_pointers.keys()):
            FatalError("Duplicity identifier on line {0}."
                       .format(current_line))
        # Save new item
        self.structure_pointers[pointer_name] = self.pointer_counter
        self.pointer_counter += 1

    def add_data_to_structure(self, data_name, current_line):
        """Add new data item into structure and generate it's unique ID."""
        if (self.data_name):
            FatalError("Only one data item allowed in structure on line {0}."
                       .format(current_line))
        # Save new item
        self.data_name = data_name

    def save_new_variable(self, variable_name, current_line):
        """Add new variable and generate it's unique ID."""
        if (variable_name in self.variables.keys()):
            FatalError("Duplicity variable on line {0}."
                       .format(current_line))
        # Save new item
        self.variables[variable_name] = str(self.variables_counter)
        self.variables_counter += 1

    def get_artmc_data(self, data):
        """Find out if data converted, if not convert."""
        data = str(data)
        if (data in self.mapped_data.keys()):
            return self.mapped_data[data]
        converted = self.convert_data(data)
        self.mapped_data[data] = converted
        return converted

    def convert_data(self, data):
        """Convert internal data to string of 0s and 1s for ARTMC."""
        self.current_data += 1
        return '"' + bin(self.current_data - 1)[2:].zfill(8) + '"'

    def get_variables(self):
        """Return list of all known variables."""
        return self.variables.keys()

    def get_data_name(self):
        """Return the name of data item in structure."""
        return self.data_name

    def get_line(self):
        """Get the next line number."""
        self.current_line += 1
        return '"' + bin(self.current_line - 1)[2:].zfill(8) + '"'

    def new_i_x_ass_y(self, x, y):
        """Add new instruction of type 'x = y'."""
        self.instructions.append(["\"x=y\"",
                                  self.get_line(),
                                  self.variables[x],
                                  self.variables[y],
                                  "to: next_line",
                                  ])

    def new_i_x_ass_null(self, x):
        """Add new instruction of type 'x = null'."""
        self.instructions.append(['"x=null"',
                                  self.get_line(),
                                  self.variables[x],
                                  "to: next_line",
                                  ])

    def new_i_x_ass_y_next(self, x, y, pointer):
        """Add new instruction of type 'x = y->pointer'."""
        n = self.structure_pointers.get(pointer, None)
        if (n is None):
            FatalError("Unknown item '{0}' in variable '{1}'"
                       .format(pointer, y))

        self.instructions.append(['"x=y.next"',
                                  self.get_line(),
                                  self.variables[x],
                                  self.variables[y],
                                  str(n),
                                  "to: next_line",
                                  ])

    def new_i_x_next_ass_null(self, x, pointer):
        """Add new instruction of type 'x->pointer = null'."""
        n = self.structure_pointers.get(pointer, None)
        if (n is None):
            FatalError("Unknown item '{0}' in variable '{1}'"
                       .format(pointer, x))

        self.instructions.append(['"x.next=null"',
                                  self.get_line(),
                                  self.variables[x],
                                  str(n),
                                  "to: next_line",
                                  ])

    def new_i_x_next_ass_y(self, x, pointer, y):
        """Add new instruction of type 'x->pointer = y'."""
        n = self.structure_pointers.get(pointer, None)
        if (n is None):
            FatalError("Unknown item '{0}' in variable '{1}'"
                       .format(pointer, x))

        self.instructions.append(['"x.next=y"',
                                  self.get_line(),
                                  self.variables[x],
                                  self.variables[y],
                                  str(n),
                                  "to: next_line",
                                  self.get_descr_num()
                                  ])

    def new_i_x_next_new(self, x, pointer):
        """Add new instruction of type 'x->pointer = malloc(...)'."""
        n = self.structure_pointers.get(pointer, None)
        if (n is None):
            FatalError("Unknown item '{0}' in variable '{1}'"
                       .format(pointer, x))

        self.instructions.append(['"x.next=new"',
                                  self.get_line(),
                                  self.variables[x],
                                  str(n),
                                  "to: next_line",
                                  self.get_descr_num(),
                                  str(1),  # TODO gen_descr
                                  ])

    def new_i_x_eq_null(self, x, succ, fail):
        """Add new instruction of type 'if x == null'."""
        self.instructions.append(['"ifx==null"',
                                  self.get_line(),
                                  self.variables[x],
                                  "to: {0}".format(succ),
                                  "to: {0}".format(fail),
                                  ])

    def new_i_x_eq_y(self, x, y, succ, fail):
        """Add new instruction of type 'if x == y'."""
        self.instructions.append(['"ifx==y"',
                                  self.get_line(),
                                  self.variables[x],
                                  self.variables[y],
                                  "to: {0}".format(succ),
                                  "to: {0}".format(fail),
                                  ])

    def new_i_goto(self, label_name):
        """Add new instruction of type 'goto'."""
        self.instructions.append(["\"goto\"",
                                  self.get_line(),
                                  "to: {0}".format(label_name),
                                  ])

    def new_i_new(self, x):
        """Add new instruction of type 'x=malloc(..)'."""
        self.instructions.append(['"new"',
                                  self.get_line(),
                                  self.variables[x],
                                  "to: next_line",
                                  ])

    def new_i_if_star(self, succ, fail):
        """Add new instruction of type 'if *'."""
        self.instructions.append(['"if*"',
                                  self.get_line(),
                                  "to: {0}".format(succ),
                                  "to: {0}".format(fail),
                                  ])

    def new_i_setdata(self, x, pointer, data, line_num):
        """Add new instruction of type 'x.data = "something"."""
        data = self.get_artmc_data(data)
        if (pointer != self.data_name):
            FatalError("Assigning data to non-data item on line {0}."
                       .format(line_num))
        self.instructions.append(['"setdata"',
                                  self.get_line(),
                                  self.variables[x],
                                  data,
                                  "to: next_line",
                                  ])

    def new_i_ifdata(self, x, data, succ, fail):
        """Add new instruction of type 'if (x.data == "something")."""
        data = self.get_artmc_data(data)
        self.instructions.append(['"ifdata"',
                                  self.get_line(),
                                  self.variables[x],
                                  data,
                                  "to: {0}".format(succ),
                                  "to: {0}".format(fail),
                                  ])

    def new_label(self, label_name):
        """Add new label."""
        self.labels[label_name] = str(self.current_line)

    def label_alias(self, aliasing, existing):
        """Add alias on two labels."""
        self.aliases[aliasing] = existing

    def finish_instructions(self):
        """Finish instruction to be outputable.

        Append exit command.
        Replace all labels.
        """
        # Finish labels aliases
        for a in self.aliases.keys():
            try:
                self.labels[a] = self.labels[self.aliases[a]]
            except:
                pass

        for a in self.aliases.keys():
            self.labels[a] = self.labels[self.aliases[a]]

        self.new_label("exit")
        self.instructions.append(['"exit"',
                                  self.get_line(),
                                  ])

        # find all jumps to labels
        for i, instruction in enumerate(self.instructions):
            for j, part in enumerate(self.instructions[i]):
                if (self.instructions[i][j].startswith("to: ")):
                    label = self.instructions[i][j][4:]

                    # generic label for jumping to next line
                    if (label == "next_line"):
                        self.instructions[i][j] = str(i+1)

                    # custom label
                    elif (label in self.labels.keys()):
                        new_v = self.labels[label]
                        if (new_v == "to: next_line"):
                                new_v = str(i+1)
                        self.instructions[i][j] = new_v

                    else:
                        FatalError("Unknown label")

    def get_info(self):
        """Return string to be written into header of program.py."""
        output = "# pointer variables are : "
        output += ", ".join('{0}={1}'
                            .format(key, val)
                            for key, val in sorted(self.variables.items()))
        output += "\n# next pointers are : "
        output += ", ".join('{0}={1}'
                            .format(key, val)
                            for key, val in sorted(self.
                                                   structure_pointers.items()))
        output += "\n# data values are : "
        output += ", ".join('{0}={1}'
                            .format(key, val)
                            for key, val in sorted(self.mapped_data.items()))
        return output

    def get_full_result(self):
        """Return full output content."""
        # get first information about variables
        result = self.get_info()

        # get the ARTMC code
        self.finish_instructions()
        code = "\ndef get_program():\n    program=[\n"
        for i in self.instructions:
            code += "        (" + ",".join(i) + "),\n"
        code = code[:-2] + "]\n"

        # get the 6 variables
        vars = ""
        vars += "    node_width={0}\n".format(len(self.variables) + 1 +
                                              self.descr_num + 2 +
                                              8)
        vars += "    pointer_num={0}\n".format(len(self.variables)+1)
        vars += "    desc_num={0}\n".format(self.descr_num)
        vars += "    next_num={0}\n".format(len(self.structure_pointers))
        vars += "    err_line=\"{0}\"\n".format("1"*8)
        vars += "    restrict_var={0}\n".format(1)  # TODO

        last_code = "\n    env=(node_width, pointer_num, desc_num, next_num,"
        last_code += " err_line,restrict_var)\n"
        last_code += "    return(program, env)"

        return result+code+vars+last_code
