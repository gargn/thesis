# File name: test_error.py
# Author: Nupur Garg
# Date created: 4/13/2017
# Python Version: 3.5


import unittest
import ast

from src.globals import *
from src.models.error import *


class Test_DecomposerError(unittest.TestCase):

    def test_config_file_not_found_error(self):
        error = FileNotFoundError("test.json")
        self.assertEqual(error.message, "FileNotFoundError: File 'test.json' not found.")

    def test_else_without_if_error(self):
        error = ElseWithoutIfError(lineno=10)
        self.assertEqual(error.message, "ElseWithoutIfError: Elif or else without an if on line 10.")