#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from src.parser import Parser
from src.generate import Generate


def parse_arguments():
    """Parse arguments.

    Return object of all arguments.
    """
    parser = argparse.ArgumentParser(description="Converter from C to ARTMC.")
    parser.add_argument("INPUT_FILE",
                        help="C source file to be converted")
    parser.add_argument("-o",
                        help="Filepath to write the ARTMC file")

    return parser.parse_args()


def main():
    """The main function."""
    args = parse_arguments()
    g = Generate()
    p = Parser(args.INPUT_FILE, g)
    p.run()
    print(g.get_full_result())


if __name__ == "__main__":
    main()
