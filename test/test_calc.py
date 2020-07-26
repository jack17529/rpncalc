"""This file is responsible for the testing of the parsing of the rpn expressions.
The ply already confirms that the grammar used to parse rpn expressions does not have any
ambiguity otherwise errors would be shown at the time of making the parser table. 
All the functionalities of the calculator has been tested in this file.

NOTE: Untested code is broken code.
"""
    
import mock
import math
import pytest
from decimal import Decimal
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
    import calc
except ModuleNotFoundError:
    from rpn import calc

class TestCalc(object):
    @pytest.mark.parametrize(
        "inp,out", [("2 3 +", 5), ("2 2/-/ +", 0),
                    ("1.1 1.2 +", Decimal("2.3"))]
    )
    def test_plus(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out",
        [("2 3 - 1 +", 0), ("2 2/-/ - 2 +", 6),
         ("1.1 1.2 - 1 -", Decimal("-1.1"))],
    )
    def test_minus(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("2 3 - 1 + 2 *", 0),
            ("2 2/-/ - 2 + 4/-/ *", -24),
            ("1.1 1.2 - 1 - 2.0 *", Decimal("-2.2")),
        ],
    )
    def test_multiply(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("2 3 - 1 + 2 * 99 /", 0),
            ("2 2/-/ - 2 + 4/-/ * 4/-/ /", 6),
            ("1.1 1.2 - 1 - 2.0 * 2 /", Decimal("-1.1")),
        ],
    )
    def test_divide(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_divide_by_zero(self):
        calc.one_time_use("2 0 /")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out", [("2 2 <<", 8), ("1/-/ 2 <<", -4),
                    ("1 0 <<", 1), ("0 1 <<", 0)]
    )
    def test_leftshift(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_leftshift_with_non_integers(self):
        calc.one_time_use("2 3 - 1 + 2 * 99 / 2 <<")
        # equals to "0.0 2 <<"
        assert config.exit_flag == 1

    def test_leftshift_with_negative_second_operand(self):
        calc.one_time_use("1/-/ 2/-/ <<")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out", [("2 2 >>", 0), ("4/-/ 2 >>", -1),
                    ("1 0 >>", 1), ("0 1 >>", 0)]
    )
    def test_rightshift(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_rightshift_with_non_integers(self):
        calc.one_time_use("2 3 - 1 + 2 * 99 / 2 >>")
        # equals to "0.0 2 >>"
        assert config.exit_flag == 1

    def test_rightshift_with_negative_second_operand(self):
        calc.one_time_use("1/-/ 2/-/ >>")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out", [("2 2 !=", 0), ("4/-/ 2 !=", 1),
                    ("1.0 1.0 !=", 0), ("1.0 1 !=", 0)]
    )
    def test_not_equal(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("2 2 ==", 1), ("4/-/ 2 ==", 0),
                    ("1.0 1.0 ==", 1), ("1.0 1 ==", 1)]
    )
    def test_equal_to(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("2 2 <=", 1), ("4/-/ 2 <=", 1),
                    ("1.0 1.0 <=", 1), ("1.0 1 <=", 1)]
    )
    def test_less_than_or_equal_to(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("2 2 >=", 1), ("4/-/ 2 >=", 0),
                    ("1.0 1.0 >=", 1), ("1.0 2 >=", 0)]
    )
    def test_greater_than_or_equal_to(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("2 2 == 1 <", 0),
            ("4/-/ 2 1/-/ * <", 1),
            ("1.0 1.0 2 / <", 0),
            ("1.0 2 <", 1),
        ],
    )
    def test_less_than(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out",
        [("2 1 + 2 >", 1), ("4/-/ 2 >", 0),
         ("1.0 1.0 0.9 / >", 0), ("1.0 1 >", 0)],
    )
    def test_greater_than(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("2 2 &", 2), ("4/-/ 2 &", 0), ("4/-/ 4 &", 4)]
    )
    def test_bit_and(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_bit_and_with_non_integers(self):
        calc.one_time_use("1.0 1.0 &")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("1 1.0 &")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out", [("2 2 |", 2), ("4/-/ 2 |", -2), ("4/-/ 4 |", -4)]
    )
    def test_bit_or(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_bit_or_with_non_integers(self):
        calc.one_time_use("1.0 1.0 |")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("1 1.0 |")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out", [("2 2 ^", 0), ("4/-/ 2 ^", -2), ("4/-/ 4 ^", -8)]
    )
    def test_bit_xor(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_bit_xor_with_non_integers(self):
        calc.one_time_use("1.0 1.0 ^")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("1 1.0 ^")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out", [("2 0 &&", 0), ("4/-/ 2 &&", 1), ("1.0 1 &&", 1)]
    )
    def test_bool_and(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("2 0 ||", 1), ("4/-/ 2 ||", 1), ("0.0 0 ||", 0)]
    )
    def test_bool_or(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("2 2 ^^", 0), ("4/-/ 2 ^^", 1),
                    ("1.0 1.0 ^^", 0), ("1.0 1 ^^", 0)]
    )
    def test_bool_xor(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out",
        [("2 2 pow", 4), ("4/-/ 2 pow", 16), ("1.0 0.9 pow", 1), ("4.7 0 pow", 1)],
    )
    def test_power(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_power_with_zero_raised_to_zero(self):
        calc.one_time_use("0.0 0.0 pow")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("0/-/ 0 pow")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("0 0/-/ pow")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("2 2 min", 2),
            ("4/-/ 2 min", -4),
            ("1.0 0.9 min", Decimal("0.9")),
            ("4.7 0 min", 0),
        ],
    )
    def test_min(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("2 2 max", 2),
            ("4/-/ 2 max", 2),
            ("1.0 0.9 max", Decimal("1.0")),
            ("4.7 0 max", Decimal("4.7")),
        ],
    )
    def test_max(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("2 2 %", 0), ("4/-/ 2 %", 0),
                    ("1.0 0.1 %", Decimal("0.0"))]
    )
    def test_mod(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_mod_by_zero(self):
        calc.one_time_use("4.7 0 %")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("0/-/ 0 %")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("2 2 log", 1),
            # ('4/-/ 2 log',1),
            # ('1.0 1.0 log',Decimal('0')),
            ("100.0 10 log", 2.0),
        ],
    )
    def test_log(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_log_negtive(self):
        calc.one_time_use("4/-/ 2 log")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("4 2/-/ log")
        assert config.exit_flag == 1

    def test_log_to_the_base_one(self):
        calc.one_time_use("1.0 1.0 log")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("3 1 log")
        assert config.exit_flag == 1

    def test_log_zero(self):
        calc.one_time_use("0 2.3 log")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("e ln", 1),
            # ('4/-/ ln',1),
            ("1.0 ln", 0),
            ("e 2 pow ln", 2.0),
        ],
    )
    def test_ln(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_log_non_positive(self):
        calc.one_time_use("4/-/ ln")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("0 ln")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("1/-/ ", -1),
            # ('4/-/ ln',1),
            ("  1.99999/-/", -1.99999),
        ],
    )
    def test_unary_minus(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out",
        [("2 --", 1), ("4/-/ --", -5), ("1.2 --", Decimal("0.2")), ("1.0 -- 2 -", -2)],
    )
    def test_decrement(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("2 ++", 3), ("4/-/ ++", -3),
                    ("1.2 ++", 2.2), ("1.0 ++ 2 +", 4)]
    )
    def test_increment(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("1! ", 0),
            # ('4/-/ ln',1),
            ("  1.99999/-/ !", 0),
        ],
    )
    def test_boolean_not(self, inp, out):
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize("inp,out", [("1~ ", -2), ("4/-/ ~", 3), ("  2~", -3), ])
    def test_bit_not(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_bit_not_floats(self):
        calc.one_time_use("4.2/-/ ~")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("0.2 ~")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("0 cosh", 1),
            ("pi 2 / cosh",
             calc.round_math(math.cosh(config.const["pi"] / 2))),
        ],
    )
    def test_cosh(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    def test_cosh_overflow(self):
        calc.one_time_use("2300.2 cosh")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("3000/-/ cosh")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("0 sinh", 0),
            ("pi 2 / sinh",
             calc.round_math(math.sinh(config.const["pi"] / 2))),
        ],
    )
    def test_sinh(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    def test_sinh_overflow(self):
        calc.one_time_use("2300.2 sinh")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("3000/-/ sinh")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("0 tanh", 0),
            ("pi 2 / tanh",
             calc.round_math(math.tanh(config.const["pi"] / 2))),
            ("pi tanh", calc.round_math(math.tanh(config.const["pi"]))),
        ],
    )
    def test_tanh(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("0.0 cos", 1), ("pi 2 / cos", 0), ("pi cos", -1)]
    )
    def test_cos(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("0.0 sin", 0), ("pi 2 / sin", 1), ("pi sin", 0)]
    )
    def test_sin(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out",
        [
            # ('0.0 acos',config.const['pi']/2),
            ("0.0 acos", 90),
            ("1 acos", 0),
        ],
    )
    def test_acos(self, inp, out):
        config.dEG, config.rAD = 1, 0
        assert calc.one_time_use(inp) == out
        config.dEG, config.rAD = 0, 1

    def test_acos_input_outside_range(self):
        calc.one_time_use("2 acos")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("3.3/-/ acos")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out",
        [("0.0 asin", 0), ("1 asin", calc.round_math(config.const["pi"] / 2))],
    )
    def test_asin(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    def test_asin_input_outside_range(self):
        calc.one_time_use("2 asin")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("3.3/-/ asin")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out",
        [("0.0 atan", 0), ("1 atan", calc.round_math(config.const["pi"] / 4))],
    )
    def test_atan(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize("inp,out", [("0.0 exp", 1), ("1 exp", config.const["e"])])
    def test_exp(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize("inp,out", [("4.0 sqrt", 2.0), ("1.44 sqrt", 1.2)])
    def test_sqrt(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    def test_sqrt_for_negatives(self):
        calc.one_time_use("2/-/ sqrt")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("3.3/-/ sqrt")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out", [("4.2 ceil", 5.0), ("1.44/-/ ceil", -1),
                    ("1.6/-/ ceil", -1)]
    )
    def test_ceil(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("4.2 floor", 4.0), ("1.44/-/ floor", -2),
                    ("1.6/-/ floor", -2)]
    )
    def test_floor(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("4.222222222 round", calc.round_math(4.222222222)),
            ("1.33333333333/-/ round", calc.round_math(-1.33333333333)),
            ("1.66666666666/-/ round", calc.round_math(-1.66666666666)),
        ],
    )
    def test_round(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("4/-/ abs", 4), ("1.44/-/ abs", 1.44), ("1 abs", 1)]
    )
    def test_abs(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("4 sign", 1), ("1.44/-/ sign", -1), ("0 sign", 0)]
    )
    def test_sign(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize("inp,out", [("4 ip", 4), ("1.44/-/ ip", -2), ("0 ip", 0)])
    def test_ip(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize(
        "inp,out", [("4 fp", 0), ("1.44/-/ fp", Decimal("0.56")), ("0 fp", 0)]
    )
    def test_fp(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    @pytest.mark.parametrize("inp,out", [("1 fact", 1), ("5 fact", 120), ("0 fact", 1)])
    def test_fact(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    def test_fact_of_floats_and_negative_integers(self):
        calc.one_time_use("2/-/ fact")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("3.3 fact")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out", [("1 hnl", 16777216), ("214748300 hnl", 2362231820)]
    )
    def test_hnl(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    def test_hnl_negative_and_floats(self):
        calc.one_time_use("2/-/ hnl")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("2.2 hnl")
        assert config.exit_flag == 1

    @pytest.mark.parametrize("inp,out", [("1 hns", 256), ("400 hns", 36865)])
    def test_hns(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    def test_hns_negative_and_floats(self):
        calc.one_time_use("2/-/ hns")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("2.2 hns")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out", [("16777216 nhl", 1), ("2362231820 nhl", 214748300)]
    )
    def test_nhl(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    def test_nhl_negative_and_floats(self):
        calc.one_time_use("2/-/ nhl")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("2.2 nhl")
        assert config.exit_flag == 1

    @pytest.mark.parametrize("inp,out", [("36865 nhs", 400), ("256 nhs", 1)])
    def test_nhs(self, inp, out):
        # config.dEG=1
        assert calc.one_time_use(inp) == out

    def test_nhs_negative_and_floats(self):
        calc.one_time_use("2/-/ nhs")
        assert config.exit_flag == 1
        config.exit_flag = 0
        calc.one_time_use("2.2 nhs")
        assert config.exit_flag == 1

    @pytest.mark.parametrize(
        "inp,out",
        [
            ("5 4 4 2     repeat +", 13),
            ("5 4 0 repeat + +", 9),
            ("5 4 + 0 repeat +", 9),
        ],
    )
    def test_repeat(self, inp, out):
        assert calc.one_time_use(inp) == out

    def test_repeat_floats_and_negatives(self):
        _, _, b = calc.repeat_func(("5 4 0.2 repeat +").split(" "), [], 1)
        assert b == 1
        _, _, b = calc.repeat_func(("5 4 1/-/ repeat +").split(" "), [], 1)
        assert b == 1

    @pytest.mark.parametrize(
        "inp,inp2,out",
        [
            (("dup").split(" "), [3], [3, 3]),
            (("  dup").split(" "), ["0b11"], ["0b11", "0b11"]),
        ],
    )
    def test_stack_manipulation_dup(self, inp, inp2, out):
        _, stac, _ = calc.stack_manipulation(inp, inp2)
        assert stac == out

    def test_stack_manipulation_dup_empty_stack(self):
        _, _, b = calc.stack_manipulation(("dup").split(" "), [])
        assert b == 1

    @pytest.mark.parametrize(
        "inp,inp2,out",
        [
            (("2 dupn").split(" "), [2, 3], [2, 3, 2, 3]),
            (
                ("  2  dupn").split(" "),
                ["0b11", "0b01"],
                ["0b11", "0b01", "0b11", "0b01"],
            ),
        ],
    )
    def test_stack_manipulation_dupn(self, inp, inp2, out):
        _, stac, _ = calc.stack_manipulation(inp, inp2)
        assert stac == out

    def test_stack_manipulation_dupn_empty_stack_negatives_floats(self):
        _, _, b = calc.stack_manipulation(("3 dupn").split(" "), [])
        assert b == 1
        _, _, b = calc.stack_manipulation(("3/-/ dupn").split(" "), [1, 2, 3])
        assert b == 1
        _, _, b = calc.stack_manipulation(
            ("3.3 dupn").split(" "), [1, 2, 3, 4])
        assert b == 1

    @pytest.mark.parametrize(
        "inp,inp2,out",
        [
            (("2 pick").split(" "), [2, 3], [2, 3]),
            (
                ("  2      pick").split(" "),
                ["0b111", "0b11", "0b01"],
                ["0b111", "0b01", "0b11"],
            ),
        ],
    )
    def test_stack_manipulation_pick(self, inp, inp2, out):
        _, stac, _ = calc.stack_manipulation(inp, inp2)
        assert stac == out

    def test_stack_manipulation_pick_from_smaller_stack_floats_negative_integers(self):
        _, _, b = calc.stack_manipulation(("2 pick").split(" "), [3])
        assert b == 1
        _, _, b = calc.stack_manipulation(
            ("1.3 pick").split(" "), [1, 2, 3, 4])
        assert b == 1
        _, _, b = calc.stack_manipulation(("1/-/ pick").split(" "), [1, 2, 3])
        assert b == 1

    @pytest.mark.parametrize(
        "inp,inp2,out",
        [
            (("drop").split(" "), [3], []),
            (("  drop").split(" "), ["0b11", "0b01"], ["0b11"]),
        ],
    )
    def test_stack_manipulation_drop(self, inp, inp2, out):
        _, stac, _ = calc.stack_manipulation(inp, inp2)
        assert stac == out

    def test_stack_manipulation_drop_from_empty_stack(self):
        _, _, b = calc.stack_manipulation((" drop").split(" "), [])
        assert b == 1

    @pytest.mark.parametrize(
        "inp,inp2,out",
        [
            (("2 dropn").split(" "), [1, 2, 3], [1]),
            ((" 3    dropn").split(" "), ["0b11", "0b01", "0xfff"], []),
        ],
    )
    def test_stack_manipulation_dropn(self, inp, inp2, out):
        _, stac, _ = calc.stack_manipulation(inp, inp2)
        assert stac == out

    def test_stack_manipulation_dropn_from_small_stack_floats_negative_integers(self):
        _, _, b = calc.stack_manipulation(("2 dropn").split(" "), [1])
        assert b == 1
        _, _, b = calc.stack_manipulation(("2.2 dropn").split(" "), [1, 2, 3])
        assert b == 1
        _, _, b = calc.stack_manipulation(("2/-/ dropn").split(" "), [1, 2, 3])
        assert b == 1

    @pytest.mark.parametrize(
        "inp,inp2,out",
        [
            ((" swap").split(" "), [1, 2, 3], [1, 3, 2]),
            (
                ("    swap").split(" "),
                ["0b11", "0b01", "0xfff"],
                ["0b11", "0xfff", "0b01"],
            ),
        ],
    )
    def test_stack_manipulation_swap(self, inp, inp2, out):
        _, stac, _ = calc.stack_manipulation(inp, inp2)
        assert stac == out

    def test_stack_manipulation_swap_smaller_stack(self):
        _, _, b = calc.stack_manipulation((" swap ").split(" "), [1])
        assert b == 1

    @pytest.mark.parametrize(
        "inp,inp2,out",
        [
            (("1 roll").split(" "), [1, 2, 3], [2, 3, 1]),
            (
                (" 2   roll").split(" "),
                ["0b11", "0b01", "0xfff"],
                ["0xfff", "0b11", "0b01"],
            ),
        ],
    )
    def test_stack_manipulation_roll(self, inp, inp2, out):
        _, stac, _ = calc.stack_manipulation(inp, inp2)
        assert stac == out

    def test_stack_manipulation_roll_floats_and_negative_integers(self):
        _, _, b = calc.stack_manipulation((" 1.2 roll ").split(" "), [1, 2, 3])
        assert b == 1
        _, _, b = calc.stack_manipulation(
            (" 1/-/ roll ").split(" "), [1, 2, 3])
        assert b == 1

    @pytest.mark.parametrize(
        "inp,inp2,out",
        [
            (("1 rolld").split(" "), [1, 2, 3], [3, 1, 2]),
            (
                (" 2   rolld").split(" "),
                ["0b11", "0b01", "0xfff"],
                ["0b01", "0xfff", "0b11"],
            ),
        ],
    )
    def test_stack_manipulation_rolld(self, inp, inp2, out):
        _, stac, _ = calc.stack_manipulation(inp, inp2)
        assert stac == out

    def test_stack_manipulation_rolld_floats_and_negative_integers(self):
        _, _, b = calc.stack_manipulation(
            (" 1.2 rolld ").split(" "), [1, 2, 3])
        assert b == 1
        _, _, b = calc.stack_manipulation(
            (" 1/-/ rolld ").split(" "), [1, 2, 3])
        assert b == 1

    def test_stack_properties(self):
        config.view = 0
        assert calc.stack_properties(("stack ").split(" ")) == True
        assert config.view == 1
        config.st = [1, 2, 3]
        assert calc.stack_properties(("depth ").split(" ")) == True
        assert config.st == [1, 2, 3, 3]

    @pytest.mark.parametrize(
        "inp,inp2,inp3,out,out2",
        [
            ({"a": 1}, ("clr ").split(" "), [1, 2, 3], {"a": 1}, []),
            (
                {"a": 1},
                ("clv").split(" "),
                ["0b11", "0b01", "0xfff"],
                {},
                ["0b11", "0b01", "0xfff"],
            ),
        ],
    )
    def test_one_word_commands(self, inp, inp2, inp3, out, out2):
        config.variables = inp
        config.st = inp3
        b = calc.clear_commands(inp2)
        assert b == True
        assert config.variables == out
        assert config.st == out2

    @pytest.mark.parametrize(
        "inp,inp2,out",
        [
            (("bin ").split(" "), (1, 0, 0, 0), (0, 1, 0, 0)),
            (("hex").split(" "), (0, 1, 0, 0), (0, 0, 0, 1)),
        ],
    )
    def test_mode_dec_bin_oct_hex(self, inp, inp2, out):
        config.dEC, config.bIN, config.oCT, config.hEX = inp2
        b = calc.check_mode(inp)
        assert b == True
        assert (config.dEC, config.bIN, config.oCT, config.hEX) == out

    @pytest.mark.parametrize(
        "inp,inp2,out",
        [(("deg ").split(" "), (1, 0), (0, 1)),
         (("rad").split(" "), (1, 0), (1, 0))],
    )
    def test_mode_rad_deg(self, inp, inp2, out):
        config.rAD, config.dEG = inp2
        b = calc.check_mode(inp)
        assert b == True
        assert (config.rAD, config.dEG) == out

    @mock.patch("random.uniform")
    def test_rand(self, random_call):
        random_call.return_value = 0.5
        assert calc.rand_func("rand".split(" ")) == ["0.5"]


if __name__ == "__main__":
    unittest.main()
