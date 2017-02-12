"""Define token types."""


class TokenEnum:
    """Enumerate for token types."""

    TAdd, TSub, TMul, TDiv, TMod, TUnaryAdd, TUnarySub, TAddE, TSubE, TMulE,\
    TDivE, TModE, TE, TN, TAnd, TAmp, TOr, TNE, TLE, TL, TGE, TG, TLZ, TPZ,\
    TInt, TDouble, TStr, TIden, TC, TD, TP, TS, TLZZ, TPZZ, TLHZ, TPHZ, TAss,\
    KWInt, KWDouble, KWChar, KWDo, KWDouble, KWElse, KWEnum, KWFloat, KWFor,\
    KWGoto, KWIf, KWInt, KWMalloc, KWNull, KWReturn, KWSizeof, KWStruct,\
    KWTypedef, KWVoid, KWWhile, XEOF = range(58)  # noqa: E122


class TokenGroups:
    """Groups of tokens, that any of them can be used in some context."""

    DataTypes = [TokenEnum.KWChar,
                 TokenEnum.KWDouble,
                 TokenEnum.KWFloat,
                 TokenEnum.KWInt,
                 TokenEnum.KWVoid,
                 ]

TokenType = {
        '+':       TokenEnum.TAdd,
        '-':       TokenEnum.TSub,
        '*':       TokenEnum.TMul,
        '/':       TokenEnum.TDiv,
        '%':       TokenEnum.TMod,
        '++':      TokenEnum.TUnaryAdd,
        '--':      TokenEnum.TUnarySub,
        '+=':      TokenEnum.TAddE,
        '-=':      TokenEnum.TSubE,
        '*=':      TokenEnum.TMulE,
        '/=':      TokenEnum.TDivE,
        '%=':      TokenEnum.TModE,
        '==':      TokenEnum.TE,
        '!':       TokenEnum.TN,
        '&&':      TokenEnum.TAnd,
        '&':       TokenEnum.TAmp,
        '||':      TokenEnum.TOr,
        '!=':      TokenEnum.TNE,
        '<=':      TokenEnum.TLE,
        '<':       TokenEnum.TL,
        '>=':      TokenEnum.TGE,
        '>':       TokenEnum.TG,
        '(':       TokenEnum.TLZ,
        ')':       TokenEnum.TPZ,
        ',':       TokenEnum.TC,
        '.':       TokenEnum.TD,
        '->':      TokenEnum.TP,
        ';':       TokenEnum.TS,
        '{':       TokenEnum.TLZZ,
        '}':       TokenEnum.TPZZ,
        '[':       TokenEnum.TLHZ,
        ']':       TokenEnum.TPHZ,
        '=':       TokenEnum.TAss,
        'char':    TokenEnum.KWChar,
        'do':      TokenEnum.KWDo,
        'double':  TokenEnum.KWDouble,
        'else':    TokenEnum.KWElse,
        'enum':    TokenEnum.KWEnum,
        'float':   TokenEnum.KWFloat,
        'for':     TokenEnum.KWFor,
        'goto':    TokenEnum.KWGoto,
        'if':      TokenEnum.KWIf,
        'int':     TokenEnum.KWInt,
        'malloc':  TokenEnum.KWMalloc,
        'NULL':    TokenEnum.KWNull,
        'return':  TokenEnum.KWReturn,
        'sizeof':  TokenEnum.KWSizeof,
        'struct':  TokenEnum.KWStruct,
        'typedef': TokenEnum.KWTypedef,
        'void':    TokenEnum.KWVoid,
        'while':   TokenEnum.KWWhile,
}
