"""Store instructions and generating output code."""

from src.error import FatalError


class Generate:
    """The class for storing and generating output code."""

    def __init__(self):
        """The init."""
        self.instructions = []

        # All items of the main data structure and it's instances
        self.structure_pointers = {}
        self.structure_data = {}
        self.variables = {}

        # A counter of unique ids
        self.pointer_counter = 0
        self.variables_counter = 0

        # A counter of lines
        self.current_line = 0

        # Dictionary of labels
        self.labels = {}

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
        self.structure_data[data_name] = str(self.pointer_counter)
        self.pointer_counter += 1

    def save_new_variable(self, variable_name):
        """Add new variable and generate it's unique ID."""
        if (variable_name in self.variables.keys()):
            FatalError("Duplicity variable on line {0}."
                       .format(self.s.get_current_line()))
        # Save new item
        self.variables[variable_name] = str(self.variables_counter)
        self.variables_counter += 1

    def get_variables(self):
        """Return list of all known variables."""
        return self.variables.keys()

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
        n = self.structure_pointers.get(pointer,
                                        self.structure_data.get(pointer,
                                                                None))
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

    def new_i_goto(self, label_name):
        """Add new instruction of type 'goto'."""
        self.instructions.append(["\"goto\"",
                                  self.get_line(),
                                  "to: {0}".format(label_name),
                                  ])

    def new_label(self, label_name):
        """Add new label."""
        self.labels[label_name] = str(self.current_line)

    def finish_instructions(self):
        """Finish instruction to be outputable.

        Append exit command.
        Replace all labels.
        """
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
                        self.instructions[i][j] = self.labels[label]

                    else:
                        FatalError("Unknown label")

    def get_info(self):
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

    def get_code(self):
        """Return converted ARTMC instructions."""
        self.finish_instructions()
        output = "def get_program():\n    program=[\n"
        for i in self.instructions:
            output += "        (" + ",".join(i) + "),\n"
        output = output[:-2] + "]"
        # TODO add other things on the end such are node_width, pointer_num...
        return output
