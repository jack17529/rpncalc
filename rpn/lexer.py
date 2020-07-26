"""
This file is responnsible for the lexer used by this rpn calculator.
"""

import ply.lex as lex

try:
    import config
except ModuleNotFoundError:
    from rpn import config


class RPNlexer(object):
    """This class has all the tokens that are to be classified by this rpn calculator.
    """    
    tokenized = []

    # List of token names.
    tokens = (
        "NAME",
        "INT",
        "FLOAT",
        "HEX",
        "OCT",
        "BIN",
        "INCREMENT",
        "PLUS",
        "MINUS",
        "MULTIPLY",
        "DIVIDE",
        "ASSIGN",
        "LEFTSHIFT",
        "DECREMENT",
        "UMINUS",
        "CHKNOTEQUAL",
        "BOOLNOT",
        "BITAND",
        "BITOR",
        "BITNOT",
        "BOOLAND",
        "BOOLXOR",
        "BITXOR",
        "POW",
        "CHKLESSOREQUAL",
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
        "MIN",
        "MAX",
        "MOD",
        "RIGHTSHIFT",
        "BOOLOR",
        "LESSTHAN",
        "GREATERTHAN",
        "EQUALTO",
        "CHKGREATEROREQUAL",
        "EXP",
        "SQRT",
        "LN",
        "LOG",
        "CEIL",
        "FLOOR",
        "ROUND",
        "IP",
        "FP",
        "SIGN",
        "ABS",
    )

    # Regular expression rules for simple tokens

    t_INCREMENT = r"\+\+"
    t_PLUS = r"\+"
    t_MINUS = r"\-"
    t_MULTIPLY = r"\*"
    t_DIVIDE = r"\/"
    t_EQUALTO = r"\=="
    t_ASSIGN = r"\="
    t_LEFTSHIFT = r"\<<"
    t_RIGHTSHIFT = r"\>>"
    t_DECREMENT = r"\--"
    t_UMINUS = r"\/-/"
    t_CHKNOTEQUAL = r"\!="  # might need change
    t_BOOLNOT = r"\!"
    t_BOOLOR = r"\|\|"
    t_BITOR = r"\|"
    t_BITNOT = r"\~"
    t_BOOLAND = r"\&&"
    t_BITAND = r"\&"
    t_BOOLXOR = r"\^\^"
    t_BITXOR = r"\^"
    t_CHKGREATEROREQUAL = r"\>="
    t_CHKLESSOREQUAL = r"\<="
    t_MOD = r"\%"
    t_LESSTHAN = r"\<"
    t_GREATERTHAN = r"\>"

    num_count = 0

    def t_HEX(self, t):
        r"0[xX][0-9a-fA-F]+"
        self.num_count += 1
        t.value = int(t.value, 0)
        return t

    def t_BIN(self, t):
        r"0[bB][0-1]+"
        self.num_count += 1
        t.value = int(t.value, 2)
        return t

    def t_OCT(self, t):
        r"0[oO][0-7]+"
        self.num_count += 1
        t.value = int(t.value, 8)
        return t

    def t_FLOAT(self, t):
        r"\d*\.\d+"
        self.num_count += 1
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r"\d+"
        self.num_count += 1
        t.value = int(t.value)
        return t

    def t_POW(self, t):
        r"pow"
        t.type = "POW"
        return t

    def t_COSH(self, t):
        r"cosh"
        t.type = "COSH"
        return t

    def t_SINH(self, t):
        r"sinh"
        t.type = "SINH"
        return t

    def t_TANH(self, t):
        r"tanh"
        t.type = "TANH"
        return t

    def t_COS(self, t):
        r"cos"
        t.type = "COS"
        return t

    def t_SIN(self, t):
        r"sin"
        t.type = "SIN"
        return t

    def t_ACOS(self, t):
        r"acos"
        t.type = "ACOS"
        return t

    def t_ASIN(self, t):
        r"asin"
        t.type = "ASIN"
        return t

    def t_ATAN(self, t):
        r"atan"
        t.type = "ATAN"
        return t

    def t_FACT(self, t):
        r"fact"
        t.type = "FACT"
        return t

    def t_HNL(self, t):
        r"hnl"
        t.type = "HNL"
        return t

    def t_HNS(self, t):
        r"hns"
        t.type = "HNS"
        return t

    def t_NHL(self, t):
        r"nhl"
        t.type = "NHL"
        return t

    def t_NHS(self, t):
        r"nhs"
        t.type = "NHS"
        return t

    def t_MIN(self, t):
        r"min"
        t.type = "MIN"
        return t

    def t_MAX(self, t):
        r"max"
        t.type = "MAX"
        return t

    def t_EXP(self, t):
        r"exp"
        t.type = "EXP"
        return t

    def t_SQRT(self, t):
        r"sqrt"
        t.type = "SQRT"
        return t

    def t_LN(self, t):
        r"ln"
        t.type = "LN"
        return t

    def t_LOG(self, t):
        r"log"
        t.type = "LOG"
        return t

    def t_CEIL(self, t):
        r"ceil"
        t.type = "CEIL"
        return t

    def t_FLOOR(self, t):
        r"floor"
        t.type = "FLOOR"
        return t

    def t_ROUND(self, t):
        r"round"
        t.type = "ROUND"
        return t

    def t_IP(self, t):
        r"ip"
        t.type = "IP"
        return t

    def t_FP(self, t):
        r"fp"
        t.type = "FP"
        return t

    def t_SIGN(self, t):
        r"sign"
        t.type = "SIGN"
        return t

    def t_ABS(self, t):
        r"abs"
        t.type = "ABS"
        return t

    def t_NAME(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        self.num_count += 1
        # t.type = 'NAME'
        return t

    t_ignore = " \t"

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        config.exit_flag = 1
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test method.
    def test(self, data):
        self.tokenized = []
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            # print(tok)
            self.tokenized.append(tok)

        return self.tokenized
