# File name: decomposer.py
# Author: Nupur Garg
# Date created: 12/25/2016
# Python Version: 3.5


from __future__ import print_function
import argparse
import ast
import sys

from src.generatecfg import CFGGenerator


# Prints AST node recursively.
def print_node(node, tabs):
    tab_str = '     '

    if not isinstance(node, ast.AST):
        return

    print('%s%s' %(tab_str*tabs, type(node)))
    for key, attr in node.__dict__.items():
        print('%s%s  ~~~  %s' %(tab_str*(tabs+1), key, attr))
        if isinstance(attr, list):
            for item in attr:
                print_node(item, tabs+2)
        else:
            print_node(attr, tabs+2)


# Prints AST structure.
def print_ast(node, debug):
    if debug:
        for child_node in node.__dict__['body']:
            print_node(child_node, tabs=0)
            print('')


# Opens and reads file.
def readfile(filename):
    f = open(filename)
    return f.read()


# Processes commandline arguments.
def process_args():
    parser = argparse.ArgumentParser(description='Code to decompose.')
    parser.add_argument('filename', help='file to parse')
    parser.add_argument('--debug', action='store_true', help='print debug messages')
    args = parser.parse_args()
    return args


# Commands to run program:
#    python -m src.decomposer codesample/python2/simple_str.py
#    python3 -m src.decomposer codesample/python3/simple_str.py
#
#    python -m src.decomposer codesample/python2/simple_loop.py
#    python3 -m src.decomposer codesample/python3/simple_loop.py
#
#    python -m src.decomposer codesample/python2/nested_for_loop.py
#
#    python -m src.decomposer codesample/python2/conditional_with_elif.py
#    python3 -m src.decomposer codesample/python3/conditional_with_elif.py
#
#    python -m src.decomposer codesample/python2/hw4_cast_1.py --debug
#
def main():
    args = process_args()
    source = readfile(args.filename)

    # Generate AST.
    node = ast.parse(source)
    print_ast(node, args.debug)

    # Generate CFG.
    generator = CFGGenerator(args.debug)
    cfg = generator.generate(node)
    print(cfg)


if __name__ == '__main__':
    main()
