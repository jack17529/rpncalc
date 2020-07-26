"""This file is responsible for the testing of the lexer used from ply. I have used
both the pytest and unittest to test the lexer.py file.
I have tried to test all the lexer functions in the lexer class in this file. Some of the
functions are left because if the parser gives a 100% test coverage, but that
can't be possible if the lexer already fails to make the tokens of the expressions.
"""
    
import pytest
import unittest

# including the root directory of the project, so there are no import errors.
import sys
import os
from pathlib import Path
sys.path.append(str(Path(Path(os.path.realpath(__file__)).parent).parent))

try:
    import config
except ModuleNotFoundError:
    from rpn import config

try:
    import lexer
except ModuleNotFoundError:
    from rpn import lexer

class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = lexer.RPNlexer()
        self.tokens = self.lexer.tokens
        self.lexer.build()

    def test_int_float_op(self):
        self.lexer.test("2 3.2 ^^")
        # print(self.lexer.tokenized)
        self.assertEqual(len(self.lexer.tokenized), 3)
        self.assertEqual(str(self.lexer.tokenized[0].type), "INT")
        self.assertEqual(self.lexer.tokenized[0].value, 2)
        self.assertEqual(str(self.lexer.tokenized[1].type), "FLOAT")
        self.assertEqual(self.lexer.tokenized[1].value, 3.2)
        self.assertEqual(str(self.lexer.tokenized[2].type), "BOOLXOR")
        self.assertEqual(self.lexer.tokenized[2].value, "^^")

    def test_hex_unaryminus_assignement(self):
        self.lexer.test("0x11/-/ x11=")
        # print(self.lexer.tokenized)
        self.assertEqual(len(self.lexer.tokenized), 4)
        self.assertEqual(str(self.lexer.tokenized[0].type), "HEX")
        self.assertEqual(self.lexer.tokenized[0].value, 17)
        self.assertEqual(str(self.lexer.tokenized[1].type), "UMINUS")
        self.assertEqual(self.lexer.tokenized[1].value, "/-/")
        self.assertEqual(str(self.lexer.tokenized[2].type), "NAME")
        self.assertEqual(self.lexer.tokenized[2].value, "x11")
        self.assertEqual(str(self.lexer.tokenized[3].type), "ASSIGN")
        self.assertEqual(self.lexer.tokenized[3].value, "=")

    # pytest -rxXs
    @pytest.mark.xfail
    def test_non_decimal_float(self):
        # Binary/Octal/Hexadecimal float type is not implemented yet.
        # It will be present in Version 1.1.0
        self.lexer.test("0B101.11 x=")
        self.assertEqual(config.exit_flag, 1)
        self.assertEqual(len(self.lexer.tokenized), 3)


if __name__ == "__main__":
    unittest.main()
