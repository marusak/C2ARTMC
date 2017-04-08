"""Lexical parser.

To initialize add source file.
Then calling get_token returns new token or None if EOF.
"""

import re
from src.tokens import TokenEnum, TokenType
from src.error import FatalError


class Scanner:
    """The lexical scanner."""

    def __init__(self, file_name):
        """The init."""
        # Read the file and format it
        self.source = preprocess(file_name)

        # Keep the last parsed value
        self.last_value = ""

        # Keep the line number for better error messages
        self.line_number = 1

        # A token that was returned into stream
        self.ungeted = None

    def get_current_line(self):
        """Return current line for error printing pursposes."""
        return self.line_number

    def get_value(self):
        """Return last parsed value."""
        return self.last_value

    def unget_token(self, token):
        """Return one token into stream."""
        self.ungeted = token

    def get_token(self):
        """Get new token."""
        if (self.ungeted):
            token = self.ungeted
            self.ungeted = None
            return token

        # Remove white spaces from beginning of string
        self.source = self.source.lstrip(' ')

        # Decide by first character
        first_char = self.source[0]

        # Check if not end of file
        if first_char == '\t':
            return TokenEnum.XEOF

        # Count lines
        if first_char == '\n':
            self.line_number += 1
            self.source = self.source[1:]
            return self.get_token()

        # If first character cannot be composed of more characters
        elif first_char in [';', ',', '(', ')', '{', '}', '[', ']', '.', ':']:
            self.source = self.source[1:]
            return TokenType[first_char]

        # Check for && or &
        elif first_char == '&':
            if self.source[1] != first_char:
                self.source = self.source[1:]
                return TokenType['&']
            else:
                self.source = self.source[2:]
                return TokenType['&&']

        # Check for ||
        elif first_char == '|':
            if self.source[1] != first_char:
                FatalError("No support for bitwise operators at {0]."
                           .format(self.line_number))
            else:
                self.source = self.source[2:]
                return TokenType[first_char+first_char]

        # Check for ++
        elif first_char == '+' and self.source[1] == '+':
            self.source = self.source[2:]
            return TokenType['++']

        # Check for --
        elif first_char == '-' and self.source[1] == '-':
            self.source = self.source[2:]
            return TokenType['--']

        # Check for ->
        elif first_char == '-' and self.source[1] == '>':
            self.source = self.source[2:]
            return TokenType['->']

        # Check for += -= *= /= <= >= != == %=
        elif first_char in ['+', '-', '*', '/', '<', '>', '!', '=', '%']:
            if self.source[1] == '=':
                self.source = self.source[2:]
                return TokenType[first_char+'=']
            else:
                self.source = self.source[1:]
                return TokenType[first_char]

        # Check for digit
        elif first_char.isdigit():
            i = 0
            while (self.source[i].isdigit() or self.source[i] == '.'):
                i += 1
            self.last_value = self.source[0:i]
            self.source = self.source[i:]
            if '.' in self.last_value:
                return TokenEnum.TDouble
            else:
                return TokenEnum.TInt

        # Check for identifier or keyword
        elif first_char.isalpha() or first_char == '_':
            i = 0
            while (self.source[i].isalnum() or self.source[i] == '_'):
                i += 1
            self.last_value = self.source[0:i]
            self.source = self.source[i:]
            if self.last_value in list(TokenType.keys()):
                return TokenType[self.last_value]
            else:
                return TokenEnum.TIden

        # Check for string (char in '' is read as string and fact that it can
        #      be only one character is ignored
        elif first_char in ['"', '\'']:
            i = 1
            while (self.source[i] != first_char):
                i += 1
            self.last_value = self.source[0:i+1]
            self.source = self.source[i+1:]
            return TokenEnum.TStr

        else:
            FatalError("Unknown character in file: '{0}' on {1}."
                       .format(first_char, self.line_number))


def preprocess(file_name):
    r"""Preprocess source file and return string.

    Preporcessing includes:
        - Remove comments -> replace by \n
        - Remove includes -> replace by \n
        - Delete all \t
        - Simplify expressions
    """
    # Read file into variable
    with open(file_name, 'r') as source_file:
        data = source_file.read()

    # Delete all one line comments - starting with //
    for comm in re.findall(r'\/\/.*?\n', data):
        data = data.replace(comm, '\n')

    # Delete all multi line comments
    for comm in re.findall(r'\/\*[\s\S]*?\*\/', data):
        data = data.replace(comm, '\n'*comm.count('\n'))

    # Delete all includes
    for incl in re.findall(r'#include.*?\n', data):
        data = data.replace(incl, '\n')

    # Delete all defines
    for incl in re.findall(r'#define.*?\n', data):
        data = data.replace(incl, '\n')

    # Delete all tabulators
    data = data.replace('\t', '')

    # Add tabulator at the end - meaning end of file
    data = data + "\t"

    return data
