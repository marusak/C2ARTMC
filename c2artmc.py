#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The main executbale."""

import sys
import argparse

from src.parser import Parser
from src.generate import Generate
from src.error import warning


def parse_arguments():
    """Parse arguments.

    Return object of all arguments.
    """
    parser = argparse.ArgumentParser(description="Converter from C to ARTMC.")
    parser.add_argument("INPUT_FILE",
                        help="C source file to be converted")
    parser.add_argument("-o",
                        help="Filepath to write the ARTMC file")
    parser.add_argument("-d",
                        help="Initial pointer descriptor")
    parser.add_argument("-i", action="store_true",
                        help="Ignore data")

    return parser.parse_args()


def main():
    """The main function."""
    args = parse_arguments()
    gen = Generate(args.d)
    parser = Parser(args.INPUT_FILE, gen, args.i)
    parser.run()

    if not args.o:
        args.o = "program.py"

    try:
        input_file = open(args.o, "w")
    except IOError:
        warning("Cannot open output file. Using stdout instead")
        input_file = sys.stdout

    input_file.write(gen.get_full_result())
    input_file.close()

if __name__ == "__main__":
    main()
