"""
This file contains the code for parser and the different functionalities present in the
calculator. The flow of the application is from calc.py to io.py
"""

import sys
import math
from collections import deque
import socket
import ply.yacc as yacc
import decimal
import random

try:
    import lexer
except ModuleNotFoundError:
    from rpn import lexer
try:
    import config
except ModuleNotFoundError:
    from rpn import config
try:
    from rpn.custom_errors import (
        ZeroDivision,
        Type,
        Value,
        ZeroRaisedToZero,
        Infinite,
        ConversionToBase10,
        OneWordCommand,
        Overflow,
    )
except ModuleNotFoundError:
    from custom_errors import (
        ZeroDivision,
        Type,
        Value,
        ZeroRaisedToZero,
        Infinite,
        ConversionToBase10,
        OneWordCommand,
        Overflow,
    )

# building the lexer.
rpn_lexer = lexer.RPNlexer()
tokens = rpn_lexer.tokens
rpn_lexer.build()


def round_math(num) -> decimal:
    """rounds the number provided according to the decimal precision.
    Uses the round half up technique to round floating points to the decimal precision.
    Args:
        num : can be of float or decimal type

    Returns:
        decimal : returns the decimal upto the decimal places told by the user
    """
    context = decimal.getcontext()
    context.rounding = decimal.ROUND_HALF_UP
    val = decimal.Decimal(str(num)) if isinstance(num, float) else num
    return round(val, config.decimal_precesion)


# def checkName(n) -> str:
#     var_name = 0
#     try:
#         if n in config.const:
#             var_name=config.const[n]
#             return var_name
#         var_name = config.variables[n]
#     except LookupError:
#         print("Undefined variable or macro name '%s'" % n)
#         config.exit_flag=1
#     return var_name

# Parsing rules


def p_statement_expression(p):
    "statement : expression"
    config.ans = p[1]


def p_statement_name_binop(p):
    """expression : expression NAME ASSIGN
    """
    if p[3] == "=":
        if p[2] in config.all_names_used:
            print(
                f"{config.bcolors.FAIL}You can't declare a constant with the name{config.bcolors.ENDC}",
                p[2],
            )
            print(
                f"{config.bcolors.OKBLUE}Use a name not present in {config.bcolors.ENDC}",
                config.all_names_used,
            )
        else:
            config.variables[p[2]] = p[1]
        config.exit_flag = 1


def p_expression_binop(p):
    """expression : expression expression PLUS
                | expression expression MINUS
                | expression expression MULTIPLY
                | expression expression DIVIDE
                | expression expression LEFTSHIFT
                | expression expression CHKNOTEQUAL
                | expression expression BITAND
                | expression expression BOOLOR
                | expression expression BITOR
                | expression expression BOOLAND
                | expression expression BOOLXOR
                | expression expression POW
                | expression expression CHKLESSOREQUAL
                | expression expression CHKGREATEROREQUAL
                | expression expression MIN
                | expression expression MAX
                | expression expression MOD
                | expression expression BITXOR
                | expression expression RIGHTSHIFT
                | expression expression LESSTHAN
                | expression expression GREATERTHAN
                | expression expression EQUALTO
                | expression expression LOG
    """

    # Converting the floating points to decimal type to get accurate results.
    p[1] = decimal.Decimal(str(p[1])) if isinstance(p[1], float) else p[1]
    p[2] = decimal.Decimal(str(p[2])) if isinstance(p[2], float) else p[2]

    if p[3] == "+":
        # plus
        p[0] = p[1] + p[2]
    elif p[3] == "-":
        # minus
        p[0] = p[1] - p[2]
    elif p[3] == "*":
        # mulitply
        p[0] = p[1] * p[2]
    elif p[3] == "/":
        # divide
        try:
            p[0] = p[1] / p[2]
        except ZeroDivisionError:
            # Example: '2 0 /'
            print(ZeroDivision("Divide", "Answer is undefined"))
            p[0] = 1
            config.exit_flag = 1
    elif p[3] == "<<":
        # left shift
        try:
            p[0] = p[1] << p[2]
        except ValueError:
            #'0.0 2 <<'
            print(Value("Left Shift", "The second operand can't be a negative integer"))
            p[0] = 1
            config.exit_flag = 1
        except TypeError:
            #'1/-/ 2/-/ <<'
            print(Type("Left Shift", "both operands", "integers"))
            p[0] = 1
            config.exit_flag = 1
    elif p[3] == "!=":
        # not equal to
        p[0] = 1 if p[1] != p[2] else 0
    elif p[3] == "||":
        # bool or
        p[0] = 1 if p[1] or p[2] else 0
    elif p[3] == "|":
        # bit or
        try:
            p[0] = p[1] | p[2]
        except TypeError:
            #'1.0 1.0 |'
            print(Type("Bitwise OR", "both operands", "integers"))
            p[0] = 1
            config.exit_flag = 1
    elif p[3] == "&&":
        # bool and
        p[0] = 1 if p[1] and p[2] else 0
    elif p[3] == "&":
        # bit and
        try:
            p[0] = p[1] & p[2]
        except TypeError:
            #'1 1.0 &'
            print(Type("Bitwise AND", "both operands", "integers"))
            config.exit_flag = 1
            p[0] = 1
    elif p[3] == "^^":
        # bool xor
        p[0] = 1 if p[1] != p[2] else 0
    elif p[3] == "pow":
        # power
        if (
            (p[1] == 0 and p[2] == 0)
            or (p[1] == -0 and p[2] == 0)
            or (p[1] == 0 and p[2] == -0)
        ):
            #'0.0 0.0 pow'
            #'0/-/ 0 pow'
            #'0 0/-/ pow'
            print(ZeroRaisedToZero("Power", "Undefined according to math"))
            config.exit_flag = 1
            p[0] = 1
        else:
            p[0] = p[1] ** p[2]
    elif p[3] == "<=":
        # less than or equal to
        p[0] = 1 if p[1] <= p[2] else 0
    elif p[3] == ">=":
        # greater than or equal to
        p[0] = 1 if p[1] >= p[2] else 0
    elif p[3] == "min":
        # minimum
        p[0] = min(p[1], p[2])
    elif p[3] == "max":
        # maximum
        p[0] = max(p[1], p[2])
    elif p[3] == "%":
        # modulous
        try:
            p[0] = p[1] % p[2]
        except ZeroDivisionError:
            #'0/-/ 0 %'
            print(ZeroDivision("Modulous", "Remainder is undefined"))
            config.exit_flag = 1
            p[0] = 1
        except decimal.InvalidOperation:
            #'4.7 0 %'
            print(ZeroDivision("Modulous", "Remainder is undefined"))
            config.exit_flag = 1
            p[0] = 1

    elif p[3] == "^":
        # bitwise xor
        try:
            p[0] = p[1] ^ p[2]
        except TypeError:
            #'1 1.0 ^'
            print(Type("Bitwise XOR", "both operands", "integers"))
            config.exit_flag = 1
            p[0] = 1
    elif p[3] == ">>":
        # right shift
        try:
            p[0] = p[1] >> p[2]
        except ValueError:
            #'1/-/ 2/-/ >>'
            print(
                Value("Right Shift", "The second operand can't be a negative integer")
            )
            p[0] = 1
            config.exit_flag = 1
        except TypeError:
            # "0.0 2 >>"
            print(Type("Right Shift", "both operands", "integers"))
            p[0] = 1
            config.exit_flag = 1
    elif p[3] == "<":
        # less than
        p[0] = 1 if p[1] < p[2] else 0
    elif p[3] == ">":
        # greater than
        p[0] = 1 if p[1] > p[2] else 0
    elif p[3] == "==":
        # equal to
        p[0] = 1 if p[1] == p[2] else 0
    elif p[3] == "log":
        # logarithm
        try:
            p[0] = math.log(p[1], p[2])
        except ValueError:
            #'4/-/ 2 log'
            print(
                Value("Logarithm", "You can't calculate log with non positive numbers")
            )
            p[0] = 1
            config.exit_flag = 1
        except ZeroDivisionError:
            #'3 1 log'
            print(ZeroDivision("Logarithm", "Answer is undefined"))
            p[0] = 1
            config.exit_flag = 1


def p_expression_unop(p):
    """expression : expression UMINUS
                    | expression DECREMENT
                    | expression BOOLNOT
                    | expression BITNOT
                    | expression COSH
                    | expression SINH
                    | expression TANH
                    | expression COS
                    | expression SIN
                    | expression ACOS
                    | expression ASIN
                    | expression ATAN
                    | expression FACT
                    | expression HNL
                    | expression HNS
                    | expression NHL
                    | expression NHS
                    | expression INCREMENT
                    | expression EXP
                    | expression LN
                    | expression SQRT
                    | expression CEIL
                    | expression FLOOR
                    | expression ROUND
                    | expression ABS
                    | expression SIGN
                    | expression IP
                    | expression FP
    """

    if p[2] == "/-/":
        # Unary minus
        p[0] = -p[1]
    elif p[2] == "--":
        # Decrement operator
        p[1] = decimal.Decimal(str(p[1])) if isinstance(p[1], float) else p[1]
        p[0] = p[1] - 1
    elif p[2] == "!":
        # Boolean NOT
        p[0] = 1 if int(p[1]) == 0 else 0
    elif p[2] == "~":
        # Bitwise NOT
        try:
            p[0] = ~(p[1])
        except TypeError:
            #'0.2 ~'
            print(Type("Negation", "operand", "integer"))
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "cosh":
        # Hyperbolic Cosine
        try:
            if config.dEG == 1:
                p[0] = round_math(math.cosh(math.radians(p[1])))
            else:
                p[0] = round_math(math.cosh(p[1]))
        except OverflowError:
            #'2300.2 cosh'
            print(config.POSITIVE_INFINITY)
            print(Infinite("Hyperbolic Cosine", "The output is too large"))
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "sinh":
        # Hyperbolic Sine
        try:
            if config.dEG == 1:
                p[0] = round_math(math.sinh(math.radians(p[1])))
            else:
                p[0] = round_math(math.sinh(p[1]))
        except OverflowError:
            #'2300.2 sinh'
            if p[1] > 0:
                print(config.POSITIVE_INFINITY)
                print(Infinite("Hyperbolic Sine", "The output is too large"))
            else:
                print(config.NEGATIVE_INFINITY)
                print(Infinite("Hyperbolic Sine",
                               "The output is too Negatively large"))
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "tanh":
        # Hyperbolic Tan
        p[0] = (
            round_math(math.tanh(math.radians(p[1])))
            if config.dEG == 1
            else round_math(math.tanh(p[1]))
        )
    elif p[2] == "cos":
        # Cosine
        p[0] = (
            round_math(math.cos(math.radians(p[1])))
            if config.dEG == 1
            else round_math(math.cos(p[1]))
        )
    elif p[2] == "sin":
        # Sine
        p[0] = (
            round_math(math.sin(math.radians(p[1])))
            if config.dEG == 1
            else round_math(math.sin(p[1]))
        )
    elif p[2] == "acos":
        # Arc Cosine
        if p[1] <= 1 and p[1] >= -1:
            p[0] = math.degrees(
                math.acos(p[1])) if config.dEG == 1 else math.acos(p[1])
        else:
            print(
                f"{config.bcolors.FAIL}The input to acos() function should be in [-1,1]{config.bcolors.ENDC}"
            )
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "asin":
        # Arc Sine
        if p[1] <= 1 and p[1] >= -1:
            p[0] = (
                round_math(math.degrees(math.asin(p[1])))
                if config.dEG == 1
                else round_math(math.asin(p[1]))
            )
        else:
            print(
                f"{config.bcolors.FAIL}The input to asin() function should be in [-1,1]{config.bcolors.ENDC}"
            )
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "atan":
        # Arc Tan
        p[0] = (
            round_math(math.degrees(math.atan(p[1])))
            if config.dEG == 1
            else round_math(math.atan(p[1]))
        )
    elif p[2] == "fact":
        # Factorial
        try:
            p[0] = math.factorial(p[1])
        except ValueError:
            #'2/-/ fact'
            print(Value("Factorial", "It works only for non negative integers"))
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "hnl":
        # Host to network long
        # Convert a 32 bit integer from host byte order to network byte order
        try:
            p[0] = socket.htonl(p[1])
        except OverflowError:
            # 2/-/ hnl
            if p[1] < 0:
                print(
                    Overflow(
                        "Host to Network Long",
                        "Operand should be positive integer only",
                    )
                )
                p[0] = 1
                config.exit_flag = 1
            else:
                print(Infinite("Host to network long", "The input is too large"))
                p[0] = 1
                config.exit_flag = 1
        except TypeError:
            # 2.2 hnl
            print(Type("Host to network long", "operand", "positive integer"))
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "hns":
        # Host to network short
        # Convert a 16 bit integer from network byte order to host byte order
        try:
            p[0] = socket.htons(p[1])
        except OverflowError:
            # 2/-/ hns
            print(
                Overflow(
                    "Host to Network Short", "Operand should be positive integer only"
                )
            )
            p[0] = 1
            config.exit_flag = 1
        except TypeError:
            # 2.2 hns
            print(Type("Host to network short", "operand", "positive integer"))
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "nhl":
        # Network to host long
        # Convert a 32 bit integer from network byte order to host byte order
        try:
            p[0] = socket.ntohl(p[1])
        except OverflowError:
            # 2/-/ nhl
            print(
                Overflow(
                    "Network to Host Long", "Operand should be positive integer only"
                )
            )
            p[0] = 1
            config.exit_flag = 1
        except TypeError:
            # 2.2 nhl
            print(Type("Network to host long", "operand", "positive integer"))
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "nhs":
        # Network to host short
        # Convert a 16 bit integer from network byte order to host byte order
        try:
            p[0] = socket.ntohs(p[1])
        except OverflowError:
            # 2/-/ nhs
            print(
                Overflow(
                    "Network to Host Short", "Operand should be positive integer only"
                )
            )
            p[0] = 1
            config.exit_flag = 1
        except TypeError:
            # 2.2 nhs
            print(Type("Network to host short", "operand", "positive integer"))
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "++":
        # Increment Operator
        p[0] = p[1] + 1
    elif p[2] == "exp":
        # Exponentiation
        p[0] = math.exp(p[1])
    elif p[2] == "ln":
        # natural logarithm
        # p[1] = decimal.Decimal(str(p[1])) if isinstance(p[1],float) else p[1]
        try:
            p[0] = round_math(math.log(p[1]))
        except ValueError:
            print(Value("Natural Logarithm", "It works only for positive numbers"))
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "sqrt":
        # Square root
        try:
            p[0] = math.sqrt(p[1])
        except ValueError:
            # When taking saqre root of negative numbers.
            print(Value("Square root", "It works only for non negative numbers"))
            p[0] = 1
            config.exit_flag = 1
    elif p[2] == "ceil":
        # Ceil
        p[0] = math.ceil(p[1])
    elif p[2] == "floor":
        # Floor
        p[0] = math.floor(p[1])
    elif p[2] == "round":
        # Round
        p[0] = round_math(p[1])
    elif p[2] == "abs":
        # Absolute
        p[0] = abs(p[1])
    elif p[2] == "sign":
        # Sign
        p[0] = 0 if p[1] == 0 else math.copysign(1, p[1])
    elif p[2] == "ip":
        # Integer part
        _, p[0] = math.modf(p[1])
        if p[1] < 0:
            p[0]-=1
        p[0]=int(p[0])
    elif p[2] == "fp":
        # Factional part
        _, integer_part = math.modf(p[1])
        p[1] = decimal.Decimal(str(p[1])) if isinstance(p[1], float) else p[1]
        if p[1]<0:
            integer_part-=1
        integer_part=int(integer_part)
        p[0] = p[1] - decimal.Decimal(str(integer_part))


def p_expression_name(p):
    "expression : NAME"
    if p[1] in config.const:
        p[0] = config.const[p[1]]
    elif p[1] in config.variables:
        p[0] = config.variables[p[1]]
    else:
        print(
            f"{config.bcolors.WARNING}Undefined variable or macro name '%s'{config.bcolors.ENDC}"
            % p[1]
        )
        p[0] = 1
        config.exit_flag = 1


def p_expression_int_float_hex_bin(p):
    """
    expression : INT
                | FLOAT
                | BIN
                | HEX
                | OCT
    """
    p[0] = p[1]


def p_error(p):
    # there should be only 1 "!=" comparision sign in a statement and no more.
    if p:
        print(
            f"{config.bcolors.FAIL}Syntax error at '%s'{config.bcolors.ENDC}" % p.value
        )
    else:
        print(f"{config.bcolors.FAIL}Syntax error at EOF{config.bcolors.ENDC}")


# yacc.yacc()


def is_number(num) -> bool:
    try:
        float(num)  # Type-casting the string to `float`.
        # If string is not a valid `float`,
        # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True


def print_dic(dic):
    """
    Prints the dictionary.

    Args:
        dic (dict): [takes a dictionary type data as input]
    """

    print("[ ", end="")
    for key, value in dic.items():
        print(key, "=", value, end=" ")
    print("]", end=" ")


def count_more_operands_needed(a) -> int:
    """Takes the string and finds out the number of operands needed,
    based on the number of binary operators and unary operators.

    Args:
        a (str): a is the string supplied by the user

    Returns:
        int: the number of operands that need to be taken from the stack
    """

    rpn_lexer.num_count = 0
    rpn_lexer.lexer.input(a)
    tot = 0
    while True:
        tok = rpn_lexer.lexer.token()
        if not tok:
            break
        if str(tok.type) in config.unary_tokens:
            continue
        if str(tok.type) in rpn_lexer.tokens:
            tot += 1

    return (tot - int(rpn_lexer.num_count)) + 1 - int(rpn_lexer.num_count)


def stack_value(i) -> str:
    """Converts the supplied input into a base 10 representation of the
    number in the string form.

    Args:
        i can be of any type, int , float, string or decimal type.

    Returns:
        str: string which is the base 10 repesentation of 'i'
    """
    val = ""
    if isinstance(i, str):
        if i.__contains__(".") and any((config.bIN, config.hEX, config.oCT)):
            print(
                f"{config.bcolors.WARNING}Calculations with non decimal floats like ",
                i,
                " will be avialable in version 0.2.0{config.bcolors.ENDC}",
            )
            config.exit_flag = 1
            val = "0"
        # check whether it is from hex or bin.
        elif (i[:2] == "0b") or (i[:2] == "0B"):
            try:
                val = str(int(i, 2))
            except ValueError:
                print(ConversionToBase10(str(i), "binary"))
        elif (i[:3] == "-0b") or (i[:3] == "-0B"):
            try:
                val = str(abs(int(i, 2))) + "/-/ "
            except ValueError:
                print(ConversionToBase10(str(i), "binary"))
        elif (i[:2] == "0x") or (i[:2] == "0X"):
            try:
                val = str(int(i, 0))
            except ValueError:
                print(ConversionToBase10(str(i), "hexadecimal"))
        elif (i[:3] == "-0x") or (i[:3] == "-0X"):
            try:
                val = str(abs(int(i, 0))) + "/-/ "
            except ValueError:
                print(ConversionToBase10(str(i), "hexadecimal"))
        elif (i[:2] == "0o") or (i[:2] == "0O"):
            try:
                val = str(int(i, 8))
            except ValueError:
                print(ConversionToBase10(str(i), "octal"))
        elif (i[:3] == "-0o") or (i[:3] == "-0O"):
            try:
                val = str(abs(int(i, 8))) + "/-/ "
            except ValueError:
                print(ConversionToBase10(str(i), "octal"))
        else:
            val = str(i)
    elif (
        (isinstance(i, int))
        or (isinstance(i, float))
        or (isinstance(i, decimal.Decimal))
    ):
        if i < 0:
            j = i * (-1)
            val = str(j) + "/-/"
        else:
            val = str(i)

    return val


yacc.yacc()


def make_str(stac) -> str:
    """Given an arry it removes the extra spaces and forms a string.

    Args:
        stac (list): stac is the name of the array.

    Returns:
        str: res is the resulting string of the array.
    """

    res = ""
    for i in stac:
        if i != "":
            res += stack_value(i) + " "
    return res


# def decimal_converter(num, zeros):
#     while num > 1:
#         num /= 10
#     for _ in range(zeros):
#         num /=10
#     return num 

# def float_bin(number, places = 6):

#     ip, fp = str(number).split(".")
#     ip = int(ip)
#     zeros = fp.count('0')
#     fp = int(fp)

#     binary_string = bin(ip) + "."

#     for _ in range(places):
#         ip, fp = str((decimal_converter(fp, zeros)) * 2.0).split(".")
#         zeros = fp.count('0')
#         fp = int(fp)
#         binary_string += ip

#     return res


def check_mode(arr) -> bool:
    """checks the mode of the rpncalc that the user wants.
    Modes in rpncalc - decimal, binary, ocatal, hexadecimal, radians and degrees.

    Args:
        arr (list): an array with all the commands passed by the user as input string.

    Returns:
        bool: returns true if the string contains a mode changing command
                else return false.
    """

    if arr[0] == "bin":
        # binary mode on.
        if len(arr) > 2:
            print(OneWordCommand("bin"))
        elif len(arr) == 2:
            if arr[1] == "":
                config.dEC, config.bIN, config.oCT, config.hEX = 0, 1, 0, 0
            else:
                print(OneWordCommand("bin"))
        else:
            config.dEC, config.bIN, config.oCT, config.hEX = 0, 1, 0, 0
        return True

    elif arr[0] == "oct":
        if len(arr) > 2:
            print(OneWordCommand("oct"))
        elif len(arr) == 2:
            if arr[1] == "":
                config.dEC, config.bIN, config.oCT, config.hEX = 0, 0, 1, 0
            else:
                print(OneWordCommand("oct"))
        else:
            config.dEC, config.bIN, config.oCT, config.hEX = 0, 0, 1, 0
        return True

    elif arr[0] == "hex":
        if len(arr) > 2:
            print(OneWordCommand("hex"))
        elif len(arr) == 2:
            if arr[1] == "":
                config.dEC, config.bIN, config.oCT, config.hEX = 0, 0, 0, 1
            else:
                print(OneWordCommand("hex"))
        else:
            config.dEC, config.bIN, config.oCT, config.hEX = 0, 0, 0, 1
        return True

    elif arr[0] == "dec":
        if len(arr) > 2:
            print(OneWordCommand("dec"))
        elif len(arr) == 2:
            if arr[1] == "":
                config.dEC, config.bIN, config.oCT, config.hEX = 1, 0, 0, 0
            else:
                print(OneWordCommand("dec"))
        else:
            config.dEC, config.bIN, config.oCT, config.hEX = 1, 0, 0, 0
        return True

    elif arr[0] == "deg":
        if len(arr) > 2:
            print(OneWordCommand("deg"))
        elif len(arr) == 2:
            if arr[1] == "":
                config.rAD, config.dEG = 0, 1
            else:
                print(OneWordCommand("deg"))
        else:
            config.rAD, config.dEG = 0, 1
        return True

    elif arr[0] == "rad":
        if len(arr) > 2:
            print(OneWordCommand("rad"))
        elif len(arr) == 2:
            if arr[1] == "":
                config.rAD, config.dEG = 1, 0
            else:
                print(OneWordCommand("rad"))
        else:
            config.rAD, config.dEG = 1, 0
        return True

    return False


def repeat_func(arr, stac, parallel):
    """repeat function is used to repeat an operator given number of times.

    Args:
        arr (list): the array of the input string given by user.
        stac (list): the stack present in the calculator.
        parallel (int): 0 means not parallel execution, 1 means parallel execution.

    Returns:
        tuple: a tuple of string, stack and int flag for the successful
                execution of the repeat function. 
    """

    s = make_str(arr)  # it's correct till here.
    s2 = ""
    arr = s.split(" ")
    if arr[len(arr) - 1] == "":
        arr = arr[:-1]
    repeat_present = 0
    repeat_error = 0
    repeat_used_stack = 0
    ind = -1

    # there should always be an operator on the right side of repeat and nothing else.
    while ind < len(arr) - 1:
        if arr[ind + 1] == "repeat":
            repeat_present = 1
            if ind + 1 == 0:
                if parallel:
                    return s, stac, 1
                try:
                    range(int(stack_value(stac[-1])))
                except TypeError:
                    print(
                        Type(
                            "Repeat",
                            "operand",
                            "non negative imteger and not negaative inetger",
                        )
                    )
                    repeat_error = 1
                    break
                except ValueError:
                    print(
                        Value(
                            "Repeat",
                            "The operands should be of non negative integers and not floats",
                        )
                    )
                    repeat_error = 1
                    break
                tmp = int(stack_value(stac[-1]))
                if tmp < 0:
                    print(
                        Type(
                            "Repeat",
                            "operand",
                            "non negative imteger and not negaative inetger",
                        )
                    )
                    repeat_error = 1
                    break
                elif tmp == 0:
                    ind += 3
                    repeat_used_stack = 1
                    continue
                repeat_used_stack = 1
                for _ in range(tmp):
                    s2 += arr[ind + 2] + " "
            else:
                try:
                    int(arr[ind])
                except ValueError:
                    print(
                        Value(
                            "Repeat",
                            "The operands should be of non negative integers and not floats",
                        )
                    )
                    repeat_error = 1
                    break
                if int(arr[ind]) < 0:
                    print(
                        Type(
                            "Repeat",
                            "operand",
                            "non negative imteger and not negaative inetger",
                        )
                    )
                    repeat_error = 1
                    break
                elif int(arr[ind]) == 0:
                    ind += 2
                    continue
                for _ in range(int(arr[ind])):
                    s2 += arr[ind + 2] + " "
            ind += 2
        else:
            if ind + 2 < len(arr):
                if arr[ind + 2] != "repeat":
                    s2 += arr[ind + 1] + " "
                    ind += 1
                else:
                    ind += 1
                    continue
            else:
                s2 += arr[ind + 1] + " "
                ind += 1

    if repeat_present == 1:
        if repeat_error == 1:
            return s, stac, 1
        s = s2

    if repeat_used_stack == 1:
        if parallel:
            return s, stac, 1
        stac = stac[:-1]

    # should return stac too.
    return s, stac, 0


def rand_func(arr2) -> list:
    """Find and assignes a random value of rand variable in the user input string.
    the random value assigned is always in between the range of 0 and 1.

    Args:
        arr2 (list): takes input as list made from the user input string.

    Returns:
        list: returns a list after replacing rand with a random value between 0 and 1.
    """

    for i in range(len(arr2)):
        # replace it with a random number between 0 and 1.
        if arr2[i] == "rand":
            arr2[i] = str(random.uniform(0, 1))

    return arr2


def stack_manipulation(arr, stac):
    """Performes all the stack manipulation functions on the user
    supplied string. This function is also responsible for filling the
    rand variable in string.

    Args:
        arr (list): [arr is the list made from the user string]
        stac (list): [stac is the calculator's stack of type list]

    Returns:
        tuple: returns a tuple of (str, list, int). String is the new user string, list is the new stack and integer can take two values 0 or 1
    """

    s, stac, b = repeat_func(arr, stac, 0)
    if b:
        return s, stac, 1

    arr2 = s.split(" ")
    arr2 = rand_func(arr2)

    operators_present = 0
    stack_manipulation_error = 0
    num_of_stack_manipulations = 0

    for i in range(len(arr2)):

        if stack_manipulation_error == 1:
            break

        if arr2[i] == "dup":
            # duplicates the top most element in the stack.

            if len(stac) == 0:
                print(
                    f"{config.bcolors.FAIL}dup can't be used when the stack is empty{config.bcolors.ENDC}"
                )
                stack_manipulation_error = 1
                break
            else:
                stac.append(stac[len(stac) - 1])
                arr2[i] = ""
                num_of_stack_manipulations += 1

        elif arr2[i] == "dupn":
            # duplicates the top n elements in the stack in order.

            if len(stac) == 0:
                print(
                    f"{config.bcolors.FAIL}dupn can't be used when the stack is empty{config.bcolors.ENDC}"
                )
                stack_manipulation_error = 1
                break

            try:
                int(arr2[i - 1])
            except ValueError:
                print(Value("dupn", "Only non negative integers are allowed"))
                stack_manipulation_error = 1
                break

            for _ in range(int(arr2[i - 1])):
                if len(stac) >= int(arr2[i - 1]):
                    stac.append(stac[-int(arr2[i - 1])])
                else:
                    print(
                        f"{config.bcolors.FAIL}Wrong usage of dupn. You can't duplicate more elements than the once present in the stack.{config.bcolors.ENDC}"
                    )
                    break
            arr2[i] = ""
            num_of_stack_manipulations += 1

        elif arr2[i] == "pick":
            # Pick the -n'th item from the stack
            try:
                int(arr2[i - 1])
            except ValueError:
                print(Value("Pick", "the operand should be non negative integer"))
                stack_manipulation_error = 1
                break

            if int(arr2[i - 1]) <= len(stac):
                stac.append(stac.pop(int(arr2[i - 1]) - 1))
                arr2[i] = ""
                num_of_stack_manipulations += 1
            else:
                print(
                    f"{config.bcolors.FAIL}Wrong usage of Pick. You can't pick outside from the range of stack.{config.bcolors.ENDC}"
                )
                stack_manipulation_error = 1
                break

        elif arr2[i] == "drop":
            # Drops the top item from the stack

            if len(stac):
                stac = stac[:-1]
                arr2[i] = ""
                num_of_stack_manipulations += 1
            else:
                print(
                    f"{config.bcolors.FAIL}Wrong usage of drop function. Stack is empty.{config.bcolors.ENDC}"
                )
                stack_manipulation_error = 1
                break

        elif arr2[i] == "dropn":
            # Drops n items from the stack

            try:
                int(arr2[i - 1])
            except ValueError:
                print(Value("Dropn", "the operand should be non negative integer"))
                stack_manipulation_error = 1
                break

            if len(stac) >= int(arr2[i - 1]):
                stac = stac[: -int(arr2[i - 1])]
                arr2[i] = ""
                num_of_stack_manipulations += 1
            else:
                print(
                    f"{config.bcolors.FAIL}Wrong usage of dropn funcrion. Stack is less in size then expected.{config.bcolors.ENDC}"
                )
                stack_manipulation_error = 1
                break

        elif arr2[i] == "swap":
            # Swap the top 2 stack items

            if len(stac) > 1:
                stac[-2], stac[-1] = stac[-1], stac[-2]
                arr2[i] = ""
                num_of_stack_manipulations += 1
            else:
                print(
                    f"{config.bcolors.FAIL}Wrong usage of swap, atleast two elements should be present in the stack.{config.bcolors.ENDC}"
                )
                stack_manipulation_error = 1
                break

        elif arr2[i] == "roll":
            # Roll the stack upwards by n

            try:
                int(arr2[i - 1])
            except ValueError:
                print(Value("roll", "the operand should be non negative integer"))
                stack_manipulation_error = 1
                break

            if int(arr2[i - 1]) >= 0:
                items = deque(stac)
                items.rotate(-int(arr2[i - 1]))
                stac = list(items)
                arr2[i] = ""
                num_of_stack_manipulations += 1
            else:
                print(
                    f"{config.bcolors.FAIL}Wrong usage of roll function. The operand should be non negative integer.{config.bcolors.ENDC}"
                )
                stack_manipulation_error = 1
                break

        elif arr2[i] == "rolld":
            # Roll the stack downwards by n

            try:
                int(arr2[i - 1])
            except ValueError:
                print(Value("rolld", "the operand should be non negative integer"))
                stack_manipulation_error = 1
                break

            if int(arr2[i - 1]) >= 0:
                items = deque(stac)
                items.rotate(int(arr2[i - 1]))
                stac = list(items)
                arr2[i] = ""
                num_of_stack_manipulations += 1
            else:
                print(
                    f"{config.bcolors.FAIL}Wrong usage of rolld function. The operand should be non negative integer.{config.bcolors.ENDC}"
                )
                stack_manipulation_error = 1
                break

        elif not is_number(arr2[i]) and arr2[i] != "":
            operators_present += 1

    if stack_manipulation_error > 0:
        return s, stac, 1

    if num_of_stack_manipulations > 0 and operators_present == 0:
        return s, stac, 1
    else:
        s = make_str(arr2)

    return s, stac, 0


def clear_commands(arr) -> bool:
    """Checks whether the user string contains clear commands.
    It is also responsible for executing those commands

    Args:
        arr (list): the user string after removing extraspaces in the form of list

    Returns:
        bool: returns True if there was a clear command, else returns False
    """

    if arr[0] == "clr":
        # clears the calculator stack.

        if len(arr) > 2:
            print(OneWordCommand("clr"))
        elif len(arr) == 2:
            if arr[1] == "":
                config.st.clear()
            else:
                print(OneWordCommand("clr"))
        else:
            config.st.clear()

        return True

    elif arr[0] == "clv":
        # clears the variable list.

        if len(arr) > 2:
            print(OneWordCommand("clv"))
        elif len(arr) == 2:
            if arr[1] == "":
                config.variables.clear()
            else:
                print(OneWordCommand("clv"))
        else:
            config.variables.clear()

        return True

    elif arr[0] == "cla":
        # Clears both variables and stack lists.

        if len(arr) > 2:
            print(OneWordCommand("cla"))
        elif len(arr) == 2:
            if arr[1] == "":
                config.st.clear()
                config.variables.clear()
            else:
                print(OneWordCommand("cla"))
        else:
            config.st.clear()
            config.variables.clear()

        return True

    return False


def stack_properties(arr) -> bool:
    """These one word command tels about the properties of stack.
    'stack' command changes the display of stack from horizontal to vertical and vice-versa.
    'depth' command pushes the length of the stack in the stack.

    Args:
        arr (list): the user string after removing extraspaces in the form of list

    Returns:
        bool: True if there was a stack property command or else False.
    """

    if arr[0] == "stack":
        if len(arr) > 2:
            print(OneWordCommand("stack"))
        elif len(arr) == 2:
            if arr[1] == "":
                if config.view == 0:
                    config.view = 1
                else:
                    config.view = 0
            else:
                print(OneWordCommand("stack"))
        else:
            if config.view == 0:
                config.view = 1
            else:
                config.view = 0

        return True

    elif arr[0] == "depth":
        if len(arr) > 2:
            print(OneWordCommand("depth"))
        elif len(arr) == 2:
            if arr[1] == "":
                (config.st).append(len(config.st))
            else:
                print(OneWordCommand("depth"))
        else:
            (config.st).append(len(config.st))

        return True

    return False


def check_macro(arr3) -> bool:
    """Checks if there is a macro name in the list made from user input string
    and stores it, if there is no other variable already using that name. If an already
    user declared macro was re-declared by the user again then it will overwrite that
    macro.

    Args:
        arr3 (list): this list is the user input string in list form.

    Returns:
        bool: if there was a 'macro', string in the list it returns True else False.
    """

    if arr3[0] == "macro":
        if arr3[1] in config.all_names_used:
            print(
                f"""{config.bcolors.FAIL}You can't define a variable/macro with name{config.bcolors.ENDC}""",
                arr3[1],
                f"""{config.bcolors.WARNING}. 
            Use some other name.{config.bcolors.ENDC}""",
            )
            print(
                f"{config.bcolors.OKBLUE}Use a name not present in {config.bcolors.ENDC}",
                config.all_names_used,
            )
            config.exit_flag = 1
            return True
        config.macros[arr3[1]] = make_str(arr3[2:])
        return True
    else:
        return False


def change_ans_by_mode(an) -> str:
    """Changes the answer to the required mode set by the user.

    Args:
        an (str): It is the answer of the rpn calculations after  

    Returns:
        str: returns the answer in the correct mode.
    """

    if config.bIN:
        an = bin(int(an))
    if config.oCT:
        an = oct(int(an))
    if config.hEX:
        an = hex(int(an))
    return an


def my_help(name_of_function):
    """My own help functionality to help user, about the functionalities present in the
    calculator.

    Args:
        name_of_function (str): name of the function or operator.
    """

    if (name_of_function in config.all_names_used) or (
        name_of_function in config.all_operators_used) or (
        name_of_function == ''
    ):
        print(
            f"""{config.bcolors.OKGREEN}
    Arithmetic Operators

      +          Add
      -          Subtract
      *          Multiply
      /          Divide
      cla        Clear the stack and variables
      clr        Clear the stack
      clv        Clear the variables
      !          Boolean NOT
      !=         Not equal to
      %          Modulus
      ++         Increment
      --         Decrement

    Bitwise Operators

      &          Bitwise AND
      |          Bitwise OR
      ^          Bitwise XOR
      ~          Bitwise NOT
      <<         Bitwise shift left
      >>         Bitwise shift right

    Boolean Operators

      &&         Boolean AND
      ||         Boolean OR
      ^^         Boolean XOR

    Comparison Operators

      <          Less than
      <=         Less than or equal to
      ==         Equal to
      >          Greater than
      >=         Greater than or equal to

    Trigonometric Functions

      acos       Arc Cosine
      asin       Arc Sine
      atan       Arc Tangent
      cos        Cosine
      cosh       Hyperbolic Cosine
      sin        Sine
      sinh       Hyperbolic Sine
      tanh       Hyperbolic tangent

    Numeric Utilities

      ceil       Ceiling
      floor      Floor
      round      Round
      ip         Integer part
      fp         Floating part
      sign       Push -1, 0, or 0 depending on the sign
      abs        Absolute value
      max        Max
      min        Min

    Display Modes

      hex        Switch display mode to hexadecimal
      dec        Switch display mode to decimal (default)
      bin        Switch display mode to binary
      oct        Switch display mode to octal

    Constants

      e          Push e
      pi         Push Pi
      rand       Generate a random number

    Mathematic Functions

      exp        Exponentiation
      fact       Factorial
      sqrt       Square Root
      ln         Natural Logarithm
      log        Logarithm
      pow        Raise a number to a power

    Networking

      hnl        Host to network long
      hns        Host to network short
      nhl        Network to host long
      nhs        Network to host short

    Stack Manipulation

      pick       Pick the -n'th item from the stack
      repeat     Repeat an operation n times, e.g. '3 repeat +'
      depth      Push the current stack depth
      drop       Drops the top item from the stack
      dropn      Drops n items from the stack
      dup        Duplicates the top stack item
      dupn       Duplicates the top n stack items in order
      roll       Roll the stack upwards by n
      rolld      Roll the stack downwards by n
      stack      Toggles stack display from horizontal to vertical
      swap       Swap the top 2 stack items

    Macros and Variables

      macro      Defines a macro, e.g. 'macro kib 1024 *'
      x=         Assigns a variable, e.g. '1024 x='

    Other

      help       Print the help message, eg. help bin
      exit       Exit the calculator

    *NOTE: Better "help" functionality is coming in Version 1.1.0 soon.
        {config.bcolors.ENDC}"""
        )
    else:
        print(
            f"{config.bcolors.FAIL}Wrong use of help function, there is no functionality named '{name_of_function}' {config.bcolors.ENDC}"
        )


def one_time_use(s):
    """This function gets called if the user wants to use the rpncalc for one time use.
    User can parse just one ron expression or parse many expressions in a pipeline
    seperated by commas ','.

    Args:
        s (str): string given by user from the args in command line.

    Returns:
        str: returns the answer to the user.
    """
    res = s
    rpn_lexer.num_count = 0

    # if we are using pipelines.
    if res.__contains__(","):
        instructions = res.split(",")
        config.ans = ""

        if check_mode(instructions[0]):
            instructions = instructions[1:]

        # process each instruction.
        for i in instructions:
            i = make_str(i.split(" "))
            arr = i.split(" ")

            if check_macro(arr):
                continue

            for j in range(len(arr)):
                if arr[j] in config.macros:
                    arr[j] = config.macros[arr[j]]
            i = make_str(arr)

            if config.ans != "" and config.exit_flag == 0:
                config.ans = change_ans_by_mode(config.ans)
                i = str(config.ans) + " " + i

            # repeat and rand function can still be used.
            # although stack functions can't be used.

            config.exit_flag = 0
            i, _, b = repeat_func(i.split(" "), [], 1)
            if b:
                sys.exit()
            arr = i.split(" ")
            i = make_str(rand_func(arr))
            yacc.parse(i)

    else:
        res, _, b = repeat_func(res.split(" "), [], 1)
        if b:
            sys.exit()

        arr = res.split(" ")
        res = make_str(rand_func(arr))
        yacc.parse(res)

    if config.ans != "" and config.exit_flag == 0:
        print(config.ans)

    return config.ans


def interactive_use():
    """
    | This function is called when user wants to calculate rpn expressions
    | interactively. The program quits if the user types 'quit' or creates an EOF error.
    """
    while 1:
        try:
            if config.variables:
                print_dic(config.variables)

            if config.exit_flag == 1 and len(config.taken_st) > 0:
                config.st.extend(config.taken_st)

            if config.ans != "" and config.exit_flag == 0:
                config.ans = change_ans_by_mode(config.ans)
                config.st.append(config.ans)

            if config.st:
                # prints the stack according to the view specified by the user.
                if config.view == 0:
                    for i in config.st:
                        print(i, end=" ")
                else:
                    for i in config.st:
                        print(i)

            # reset the variables.
            config.exit_flag = 0
            config.taken_st.clear()
            config.ans = ""

            # take input from user.
            s = input("> ")

        except EOFError:
            break

        if not s:
            continue

        elif s == "exit":
            break

        else:

            # little funny code here, removes the extra spaces in the string.
            arr = s.split(" ")
            s = make_str(arr)
            arr = s.split(" ")

            if arr[0] == "help":
                # custom help function for the rpn calculator.
                if len(arr) > 3:
                    print(
                        f"{config.bcolors.FAIL}function is a two word command.{config.bcolors.ENDC}"
                    )
                elif len(arr) == 3:
                    if arr[2] == "":
                        my_help(arr[1])
                    else:
                        print(
                            f"{config.bcolors.FAIL}help function is a two word command.{config.bcolors.ENDC}"
                        )
                else:
                    my_help(arr[1])
                continue

            if clear_commands(arr):
                continue

            if stack_properties(arr):
                continue

            if check_mode(arr):
                continue

            for i in range(len(arr)):
                if arr[i] in config.macros:
                    arr[i] = config.macros[arr[i]]

            s, config.st, b = stack_manipulation(arr, config.st)
            if b:
                continue

            arr3 = s.split(" ")
            if check_macro(arr3):
                continue

            # if there is still a string with operators remaining then
            # this code is executed.
            if s != "":
                co = count_more_operands_needed(s)
            else:
                continue

            if co < 0:
                print(
                    f"{config.bcolors.FAIL}Error: wrong use of operators in expression{config.bcolors.ENDC}"
                )
                continue
            elif co > 0:
                config.taken_st = config.st[-(co):]
                s = make_str(config.st[-(co):]) + s
                config.st = config.st[:-(co)]

        yacc.parse(s)
