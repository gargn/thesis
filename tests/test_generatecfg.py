# File name: test_generatecfg.py
# Author: Nupur Garg
# Date created: 12/26/2016
# Python Version: 3.5


import unittest
import ast

from src.globals import *
from src.models.block import Block
from src.models.instruction import InstructionType
from src.generatecfg import CFGGenerator


class TestGenerateCFG(unittest.TestCase):

    def setUp(self):
        Block._label_counter.reset()
        self.generator = CFGGenerator(False)

    def _generate_cfg(self, source):
        node = ast.parse(source)
        cfg = self.generator.generate(node)
        return cfg

    def test_no_code(self):
        source = ''
        cfg = self._generate_cfg(source)
        self.assertEqual(cfg.get_num_funcs(), 0)

    def test_simple_script(self):
        source = 'string = "hi"'
        cfg = self._generate_cfg(source)
        self.assertEqual(cfg.get_num_funcs(), 0)

    def test_instr_type_return(self):
        source = ('string0 = "hi"\n'
                  'def funcA():\n'
                  '    x = 5\n'
                  '    return x')
        cfg = self._generate_cfg(source)
        block = cfg.get_func('funcA')

        self.assertEqual(block.label, 'funcA')
        self.assertEqual(block._instructions[3].referenced, set())
        self.assertEqual(block._instructions[3].defined, set(['x']))
        self.assertEqual(block._instructions[3].instruction_type, None)
        self.assertEqual(block._instructions[4].referenced, set(['x']))
        self.assertEqual(block._instructions[4].defined, set())
        self.assertEqual(block._instructions[4].instruction_type, InstructionType.RETURN)

    def test_parameters_definitions(self):
        self.skipTest('TODO: Add test ensuring function parameters are definitions')

    def test_assignment_simple(self):
        source = ('string0 = "hi"\n'
                  'def funcA():\n'
                  '    string1 = "hi"\n'
                  '    string2, string3 = string1, "hello"\n'
                  '    string4 = string5 = "hi"\n'
                  '    print(string1)')
        cfg = self._generate_cfg(source)
        block = cfg.get_func('funcA')

        self.assertEqual(block.label, 'funcA')
        self.assertEqual(block._instructions[3].referenced, set())
        self.assertEqual(block._instructions[3].defined, set(['string1']))
        self.assertEqual(block._instructions[4].referenced, set(['string1']))
        self.assertEqual(block._instructions[4].defined, set(['string2', 'string3']))
        self.assertEqual(block._instructions[5].referenced, set())
        self.assertEqual(block._instructions[5].defined, set(['string4', 'string5']))
        self.assertEqual(block._instructions[6].referenced, set(['print', 'string1']))
        self.assertEqual(block._instructions[6].defined, set())

    def test_conditional_only_if(self):
        source = ('def funcA():\n'
                  '    x = int(input("enter test score:"))\n'
                  '    if x < 70:\n'
                  '        print("You need to retake the class.")\n'
                  '    print("Done")\n')
        cfg = self._generate_cfg(source)
        func_block = cfg.get_func('funcA')

        self.assertEqual(func_block.label, 'funcA')
        self.assertEqual(func_block._instructions[2].defined, set(['x']))
        self.assertEqual(func_block._instructions[2].referenced, set(['int', 'input']))
        self.assertEqual(func_block._instructions[3].referenced, set(['x']))
        self.assertEqual(list(func_block.successors), ['L1', 'L2'])

        if_block = func_block.successors['L1']
        self.assertEqual(if_block._instructions[4].referenced, set(['print']))
        self.assertEqual(if_block._instructions[4].defined, set())
        self.assertEqual(list(if_block.predecessors), ['funcA'])
        self.assertEqual(list(if_block.successors), ['L2'])

        exit_block = if_block.successors['L2']
        self.assertEqual(exit_block._instructions[5].referenced, set(['print']))
        self.assertEqual(exit_block._instructions[5].defined, set())
        self.assertEqual(list(exit_block.predecessors), ['L1', 'funcA'])

    def test_conditional_simple_if_elif_else(self):
        source = ('def funcA():\n'
                  '    x = int(input("enter test score:"))\n'
                  '    if x < 70:\n'
                  '        print("You need to retake the class.")\n'
                  '    elif x < 85:\n'
                  '        print("You have room for improvement.")\n'
                  '    else:\n'
                  '        print("Great job!")\n')
        cfg = self._generate_cfg(source)
        func_block = cfg.get_func('funcA')

        self.assertEqual(func_block.label, 'funcA')
        self.assertEqual(func_block._instructions[2].defined, set(['x']))
        self.assertEqual(func_block._instructions[2].referenced, set(['int', 'input']))
        self.assertEqual(func_block._instructions[3].referenced, set(['x']))
        self.assertEqual(list(func_block.successors), ['L1', 'L3'])

        if_block_1 = func_block.successors['L1']
        self.assertEqual(if_block_1._instructions[4].referenced, set(['print']))
        self.assertEqual(if_block_1._instructions[4].defined, set())
        self.assertEqual(list(if_block_1.predecessors), ['funcA'])
        self.assertEqual(list(if_block_1.successors), ['L2'])

        else_block_1 = func_block.successors['L3']
        self.assertEqual(else_block_1._instructions[5].referenced, set(['x']))
        self.assertEqual(else_block_1._instructions[5].defined, set())
        self.assertEqual(list(else_block_1.predecessors), ['funcA'])
        self.assertEqual(list(else_block_1.successors), ['L4', 'L6'])

        if_block_2 = else_block_1.successors['L4']
        self.assertEqual(if_block_2._instructions[6].referenced, set(['print']))
        self.assertEqual(if_block_2._instructions[6].defined, set())
        self.assertEqual(list(if_block_2.predecessors), ['L3'])
        self.assertEqual(list(if_block_2.successors), ['L5'])

        else_block_2 = else_block_1.successors['L6']
        self.assertEqual(else_block_2._instructions[8].referenced, set(['print']))
        self.assertEqual(else_block_2._instructions[8].defined, set())
        self.assertEqual(list(else_block_2.predecessors), ['L3'])
        self.assertEqual(list(else_block_2.successors), ['L5'])

        exit_block_2 = if_block_2.successors['L5']
        self.assertFalse(exit_block_2._instructions)
        self.assertEqual(list(exit_block_2.predecessors), ['L4', 'L6'])
        self.assertEqual(list(exit_block_2.successors), ['L2'])

        exit_block_1 = if_block_1.successors['L2']
        self.assertFalse(exit_block_1._instructions)
        self.assertEqual(list(exit_block_1.predecessors), ['L1', 'L5'])

    def test_loop_single_for(self):
        source = ('def funcA():\n'
                  '    favs = ["berry", "apple"]\n'
                  '    name = "peter"\n'
                  '    for item in favs:\n'
                  '        print("%s likes %s" % (name, item))')
        cfg = self._generate_cfg(source)
        func_block = cfg.get_func('funcA')

        self.assertEqual(func_block.label, 'funcA')
        self.assertEqual(func_block._instructions[2].defined, set(['favs']))
        self.assertEqual(func_block._instructions[3].defined, set(['name']))
        self.assertEqual(list(func_block.successors), ['L1'])

        guard_block = func_block.successors['L1']
        self.assertEqual(guard_block._instructions[4].referenced, set(['favs']))
        self.assertEqual(guard_block._instructions[4].defined, set(['item']))
        self.assertEqual(list(guard_block.predecessors), ['funcA', 'L2'])
        self.assertEqual(list(guard_block.successors), ['L2', 'L3'])

        body_block = guard_block.successors['L2']
        self.assertEqual(body_block._instructions[5].referenced, set(['print', 'item', 'name']))
        self.assertEqual(body_block._instructions[5].defined, set())
        self.assertEqual(list(body_block.predecessors), ['L1'])
        self.assertEqual(list(body_block.successors), ['L1'])

        exit_block = guard_block.successors['L3']
        self.assertFalse(exit_block._instructions)
        self.assertEqual(list(exit_block.predecessors), ['L1'])

    def test_loop_nested_for(self):
        source = ('def funcA():\n'
                  '    integers = [[1, 2], [3, 4]]\n'
                  '    for numbers in integers:\n'
                  '        for integer in numbers:\n'
                  '            print("%d " %integer)')
        cfg = self._generate_cfg(source)
        func_block = cfg.get_func('funcA')

        self.assertEqual(func_block.label, 'funcA')
        self.assertEqual(func_block._instructions[2].referenced, set())
        self.assertEqual(func_block._instructions[2].defined, set(['integers']))
        self.assertEqual(list(func_block.successors), ['L1'])
        self.assertFalse(func_block.predecessors)

        guard_block_1 = func_block.successors['L1']
        self.assertEqual(guard_block_1._instructions[3].referenced, set(['integers']))
        self.assertEqual(guard_block_1._instructions[3].defined, set(['numbers']))
        self.assertEqual(list(guard_block_1.predecessors), ['funcA', 'L6'])
        self.assertEqual(list(guard_block_1.successors), ['L2', 'L3'])

        body_start_1 = guard_block_1.successors['L2']
        self.assertFalse(body_start_1._instructions)
        self.assertEqual(list(body_start_1.predecessors), ['L1'])
        self.assertEqual(list(body_start_1.successors), ['L4'])

        guard_block_2 = body_start_1.successors['L4']
        self.assertEqual(guard_block_2._instructions[4].referenced, set(['numbers']))
        self.assertEqual(guard_block_2._instructions[4].defined, set(['integer']))
        self.assertEqual(list(guard_block_2.predecessors), ['L2', 'L5'])
        self.assertEqual(list(guard_block_2.successors), ['L5', 'L6'])

        body_2 = guard_block_2.successors['L5']
        self.assertEqual(body_2._instructions[5].referenced, set(['integer', 'print']))
        self.assertEqual(body_2._instructions[5].defined, set())
        self.assertEqual(list(body_2.predecessors), ['L4'])
        self.assertEqual(list(body_2.successors), ['L4'])

        body_end_1 = guard_block_1.predecessors['L6']
        self.assertFalse(body_end_1._instructions)
        self.assertEqual(list(body_end_1.predecessors), ['L4'])
        self.assertEqual(list(body_end_1.successors), ['L1'])

        exit_block = guard_block_1.successors['L3']
        self.assertFalse(exit_block._instructions)
        self.assertEqual(list(exit_block.predecessors), ['L1'])
        self.assertFalse(exit_block.successors)

    def test_loop_single_while(self):
        source = ('def funcA():\n'
                  '    i = 0\n'
                  '    while i < 5:\n'
                  '        i += 1')
        cfg = self._generate_cfg(source)
        func_block = cfg.get_func('funcA')

        self.assertEqual(func_block.label, 'funcA')
        self.assertEqual(func_block._instructions[2].referenced, set())
        self.assertEqual(func_block._instructions[2].defined, set(['i']))
        self.assertEqual(list(func_block.successors), ['L1'])

        guard_block = func_block.successors['L1']
        self.assertEqual(guard_block._instructions[3].referenced, set(['i']))
        self.assertEqual(guard_block._instructions[3].defined, set())
        self.assertEqual(list(guard_block.predecessors), ['funcA', 'L2'])
        self.assertEqual(list(guard_block.successors), ['L2', 'L3'])

        body_block = guard_block.successors['L2']
        self.assertEqual(body_block._instructions[4].referenced, set())
        self.assertEqual(body_block._instructions[4].defined, set(['i']))
        self.assertEqual(list(body_block.predecessors), ['L1'])
        self.assertEqual(list(body_block.successors), ['L1'])

        exit_block = guard_block.successors['L3']
        self.assertFalse(exit_block._instructions)
        self.assertEqual(list(exit_block.predecessors), ['L1'])

    def test_loop_single_list_comprehension(self):
        source = ('def funcA():\n'
                  '    x = [i for i in range(5)]\n'
                  '    print(x)\n')
        cfg = self._generate_cfg(source)
        func_block = cfg.get_func('funcA')

        self.assertEqual(func_block.label, 'funcA')
        self.assertEqual(func_block._instructions[2].defined, set(['x', 'i']))
        self.assertEqual(func_block._instructions[2].referenced, set(['i', 'range']))
        self.assertEqual(func_block._instructions[3].referenced, set(['x', 'print']))
        self.assertFalse(func_block.successors)

if __name__ == '__main__':
    unittest.main()
