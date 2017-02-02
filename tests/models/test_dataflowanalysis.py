# File name: test_dataflowanalysis.py
# Author: Nupur Garg
# Date created: 2/1/2017
# Python Version: 3.5


import unittest
import ast

from src.globals import *
from src.generatecfg import CFGGenerator
from src.models.block import Block
from src.models.dataflowanalysis import *
from src.models.blockinfo import FunctionBlockInformation, ReachingDefinitions


# Test ReachingDefinitionsAnalysis class.
class TestReachingDefinitionsAnalysis(unittest.TestCase):

    def _generate_cfg(self, source):
        node = ast.parse(source)
        generator = CFGGenerator(False)
        return generator.generate(node)

    def setUp(self):
        Block._label_counter.reset()
        source = ('def funcA():\n'              # line 1
                  '     i = 3\n'                # line 2
                  '     j = i + 1\n'            # line 3
                  '     a = j + 2\n'            # line 4
                  '     while a > 0:\n'         # line 5
                  '         i = i + 1\n'        # line 6
                  '         j = j - 1\n'        # line 7
                  '         if i != j:\n'       # line 8
                  '             a = a - 1\n'    # line 9
                  '         i = i + 1')         # line 10
        self.cfg = self._generate_cfg(source)
        self.funcA = self.cfg.get_func('funcA')

    def test_abstract(self):
        with self.assertRaises(TypeError) as context:
            IterativeDataflowAnalysis(ReachingDefinitions)
        self.assertIsNotNone(context.exception)

    def test_compute_func_gen(self):
        analysismethod = ReachingDefinitionsAnalysis()
        info = FunctionBlockInformation()
        info.init(self.funcA, ReachingDefinitions)

        func_gen = analysismethod._compute_func_gen(info)
        self.assertEqual(func_gen, {'i': set([2, 6, 10]),
                                    'j': set([3, 7]),
                                    'a': set([4, 9])})

    def test_compute_gen_kill(self):
        analysismethod = ReachingDefinitionsAnalysis()
        info = FunctionBlockInformation()
        info.init(self.funcA, ReachingDefinitions)

        func_gen = analysismethod._compute_func_gen(info)
        analysismethod._compute_gen_kill(info, func_gen)

        # funcA block.
        cur_block_info = info.get_block_info(self.funcA)
        self.assertEqual(cur_block_info.gen, {'i': set([2]),
                                              'j': set([3]),
                                              'a': set([4])})
        self.assertEqual(cur_block_info.kill, {'i': set([6, 10]),
                                               'j': set([7]),
                                               'a': set([9])})

        # L1 block.
        guard_block = self.funcA.successors['L1']
        cur_block_info = info.get_block_info(guard_block)
        self.assertEqual(len(cur_block_info.gen), 0)
        self.assertEqual(len(cur_block_info.kill), 0)

        # L2 block.
        loop_body_start_block = guard_block.successors['L2']
        cur_block_info = info.get_block_info(loop_body_start_block)
        self.assertEqual(cur_block_info.gen, {'i': set([6]),
                                              'j': set([7])})
        self.assertEqual(cur_block_info.kill, {'i': set([2, 10]),
                                               'j': set([3])})

        # L4 block.
        if_body_block = loop_body_start_block.successors['L4']
        cur_block_info = info.get_block_info(if_body_block)
        self.assertEqual(cur_block_info.gen, {'a': set([9])})
        self.assertEqual(cur_block_info.kill, {'a': set([4])})

        # L5 block.
        loop_body_end_block = loop_body_start_block.successors['L5']
        cur_block_info = info.get_block_info(loop_body_end_block)
        self.assertEqual(cur_block_info.gen, {'i': set([10])})
        self.assertEqual(cur_block_info.kill, {'i': set([2, 6])})

        # L3 block.
        exit_block = guard_block.successors['L3']
        cur_block_info = info.get_block_info(exit_block)
        self.assertEqual(len(cur_block_info.gen), 0)
        self.assertEqual(len(cur_block_info.kill), 0)

    def test_compute_info(self):
        analysismethod = ReachingDefinitionsAnalysis()
        info = analysismethod.analyze(self.funcA)

        # funcA block.
        cur_block_info = info.get_block_info(self.funcA)
        self.assertEqual(len(cur_block_info.in_block), 0)
        self.assertEqual(cur_block_info.out_block, {'i': set([2]),
                                                    'j': set([3]),
                                                    'a': set([4])})

        # L1 block.
        guard_block = self.funcA.successors['L1']
        cur_block_info = info.get_block_info(guard_block)
        self.assertEqual(cur_block_info.in_block, {'i': set([2, 10]),
                                                   'j': set([3, 7]),
                                                   'a': set([4, 9])})
        self.assertEqual(cur_block_info.out_block, {'i': set([2, 10]),
                                                    'j': set([3, 7]),
                                                    'a': set([4, 9])})

        # L2 block.
        loop_body_start_block = guard_block.successors['L2']
        cur_block_info = info.get_block_info(loop_body_start_block)
        self.assertEqual(cur_block_info.in_block, {'i': set([2, 10]),
                                                   'j': set([3, 7]),
                                                   'a': set([4, 9])})
        self.assertEqual(cur_block_info.out_block, {'i': set([6]),
                                                    'j': set([7]),
                                                    'a': set([4, 9])})

        # L4 block.
        if_body_block = loop_body_start_block.successors['L4']
        cur_block_info = info.get_block_info(if_body_block)
        self.assertEqual(cur_block_info.in_block, {'i': set([6]),
                                                   'j': set([7]),
                                                   'a': set([4, 9])})
        self.assertEqual(cur_block_info.out_block, {'i': set([6]),
                                                    'j': set([7]),
                                                    'a': set([9])})

        # L5 block.
        loop_body_end_block = loop_body_start_block.successors['L5']
        cur_block_info = info.get_block_info(loop_body_end_block)
        self.assertEqual(cur_block_info.in_block, {'i': set([6]),
                                                   'j': set([7]),
                                                   'a': set([4, 9])})
        self.assertEqual(cur_block_info.out_block, {'i': set([10]),
                                                    'j': set([7]),
                                                    'a': set([4, 9])})

        # L3 block.
        exit_block = guard_block.successors['L3']
        cur_block_info = info.get_block_info(exit_block)
        self.assertEqual(cur_block_info.in_block, {'i': set([2, 10]),
                                                   'j': set([3, 7]),
                                                   'a': set([4, 9])})
        self.assertEqual(cur_block_info.out_block, {'i': set([2, 10]),
                                                    'j': set([3, 7]),
                                                    'a': set([4, 9])})

if __name__ == '__main__':
     unittest.main()