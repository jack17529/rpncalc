"""
This file stores the value of global variables and sets the variables using a rc file 
('.rpnrc') if it is present in your home directory.
"""

import math
import sys
import configparser
from pathlib import Path

rpnrc_path = str(Path.home()) + "/.rpnrc"

# sys.path.insert(0, "../..")

ans = ""
exit_flag = 0
st = []
taken_st = []

decimal_precesion = 3
const = {"pi": math.pi, "e": math.e}

POSITIVE_INFINITY = math.inf
NEGATIVE_INFINITY = -math.inf

# dictionary of names
variables = {}
macros = {}
dEC = 1
rAD = 1
dEG = 0
bIN = 0
oCT = 0
hEX = 0
view = 0

all_names_used = [
    "clr",
    "clv",
    "cla",
    "dup",
    "dupn",
    "drop",
    "dropn",
    "repeat",
    "stack",
    "pick",
    "depth",
    "sign",
    "roll",
    "rolld",
    "swap",
    "macro",
    "help",
    "exit",
    "hnl",
    "hns",
    "nhl",
    "nhs",
    "exp",
    "fact",
    "sqrt",
    "ln",
    "log",
    "pow",
    "rand",
    "bin",
    "dec",
    "oct",
    "hex",
    "ceil",
    "floor",
    "round",
    "ip",
    "fp",
    "sign",
    "min",
    "max",
    "abs",
    "acos",
    "asin",
    "atan",
    "cos",
    "cosh",
    "sin",
    "sinh",
    "tanh",
    "rad",
    "deg",
]

all_operators_used = [
    "+",
    "-",
    "*",
    "/",
    "!",
    "!=",
    "%",
    "++",
    "--",
    "&",
    "|",
    "^",
    "~",
    "<<",
    ">>",
    "&&",
    "||",
    "^^",
    "<",
    "<=",
    ">",
    ">=",
    "==",
    "=",
]

all_const_used = ["pi", "e"]

binary_tokens = [
    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "ASSIGN",
    "LEFTSHIFT",
    "CHKNOTEQUAL",
    "BITAND",
    "BITOR",
    "BOOLAND",
    "BOOLXOR",
    "BITXOR",
    "POW",
    "CHKLESSOREQUAL",
    "MIN",
    "MAX",
    "MOD",
    "RIGHTSHIFT",
    "BOOLOR",
    "LESSTHAN",
    "GREATERTHAN",
    "EQUALTO",
    "CHKGREATEROREQUAL",
    "LOG",
]

unary_tokens = [
    "DECREMENT",
    "INCREMENT",
    "UMINUS",
    "BOOLNOT",
    "BITNOT",
    "COS",
    "SIN",
    "ACOS",
    "ASIN",
    "ATAN",
    "COSH",
    "SINH",
    "TANH",
    "FACT",
    "HNL",
    "HNS",
    "NHL",
    "NHS",
    "EXP",
    "SQRT",
    "LN",
    "CEIL",
    "FLOOR",
    "ROUND",
    "IP",
    "FP",
    "SIGN",
    "ABS",
]


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


config = configparser.ConfigParser()

try:
    config.read(rpnrc_path)

    try:
        decimal_precesion = int(config["number settings"]["decimal_precesion"])
    except ValueError:
        print(
            f"{bcolors.FAIL}decimal_precesion can only take integer values.{bcolors.ENDC}"
        )
        exit_flag = 1
    for k, v in config["constants"].items():
        if k not in all_names_used:
            const[k] = float(v)
        else:
            print(
                f"{bcolors.FAIL}You can't declare a constant with the name{bcolors.ENDC}",
                k,
            )
            print(
                f"{bcolors.OKBLUE}Use a name not present in {bcolors.ENDC}",
                all_names_used,
            )
            exit_flag = 1
except NameError:
    print(
        f"{bcolors.WARNING}No rc file('.rpnrc') is present in home directory. Default settings will be used.{bcolors.ENDC}"
    )

if exit_flag:
    sys.exit()
