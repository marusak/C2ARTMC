#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

from src.parser import Parser
from src.generate import Generate
from src.error import Warning


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

    return parser.parse_args()


def main():
    """The main function."""
    args = parse_arguments()
    g = Generate(args.d)
    p = Parser(args.INPUT_FILE, g)
    p.run()

    if not args.o:
        args.o = "program.py"

    try:
        f = open(args.o, "w")
    except:
        Warning("Cannot open output file. Using stdout instead")
        f = sys.stdout

    f.write(g.get_full_result())
    f.close()

if __name__ == "__main__":
    main()
