"""Define token types."""


class TokenEnum:
    """Enumerate for token types."""

    TAdd, TSub, TMul, TDiv, TMod, TUnaryAdd, TUnarySub, TAddE, TSubE, TMulE,\
    TDivE, TModE, TE, TN, TAnd, TAmp, TOr, TNE, TLE, TL, TGE, TG, TLZ, TPZ,\
    TInt, TDouble, TStr, TIden, TC, TD, TP, TS, TLZZ, TPZZ, TLHZ, TPHZ, TAss,\
    KWAny, KWBreak, KWContinue, KWInt, KWDouble, KWChar, KWDo, KWDouble,\
    KWElse, KWEnum, KWFalse, KWFloat, KWFor, KWGoto, KWIf, KWInt, KWMalloc,\
    KWNull, KWRandomAlloc, KWReturn, KWSizeof, KWStruct, KWTrue, KWTypedef,\
    KWVoid, KWWhile, XEOF = range(64)  # noqa: E122


class TokenGroups:
    """Groups of tokens, that any of them can be used in some context."""

    DataTypes = [TokenEnum.KWChar,
                 TokenEnum.KWDouble,
                 TokenEnum.KWFloat,
                 TokenEnum.KWInt,
                 TokenEnum.KWVoid,
                 ]

    Nondeterministic = [TokenEnum.TMul,
                        TokenEnum.KWAny]

    Datas = [TokenEnum.TStr,
             TokenEnum.TInt,
             TokenEnum.TDouble]

TokenType = {
        '+':            TokenEnum.TAdd,
        '-':            TokenEnum.TSub,
        '*':            TokenEnum.TMul,
        '/':            TokenEnum.TDiv,
        '%':            TokenEnum.TMod,
        '++':           TokenEnum.TUnaryAdd,
        '--':           TokenEnum.TUnarySub,
        '+=':           TokenEnum.TAddE,
        '-=':           TokenEnum.TSubE,
        '*=':           TokenEnum.TMulE,
        '/=':           TokenEnum.TDivE,
        '%=':           TokenEnum.TModE,
        '==':           TokenEnum.TE,
        '!':            TokenEnum.TN,
        '&&':           TokenEnum.TAnd,
        '&':            TokenEnum.TAmp,
        '||':           TokenEnum.TOr,
        '!=':           TokenEnum.TNE,
        '<=':           TokenEnum.TLE,
        '<':            TokenEnum.TL,
        '>=':           TokenEnum.TGE,
        '>':            TokenEnum.TG,
        '(':            TokenEnum.TLZ,
        ')':            TokenEnum.TPZ,
        ',':            TokenEnum.TC,
        '.':            TokenEnum.TD,
        '->':           TokenEnum.TP,
        ';':            TokenEnum.TS,
        '{':            TokenEnum.TLZZ,
        '}':            TokenEnum.TPZZ,
        '[':            TokenEnum.TLHZ,
        ']':            TokenEnum.TPHZ,
        '=':            TokenEnum.TAss,
        'any':          TokenEnum.KWAny,
        'break':        TokenEnum.KWBreak,
        'continue':     TokenEnum.KWContinue,
        'char':         TokenEnum.KWChar,
        'do':           TokenEnum.KWDo,
        'double':       TokenEnum.KWDouble,
        'else':         TokenEnum.KWElse,
        'enum':         TokenEnum.KWEnum,
        'false':        TokenEnum.KWFalse,
        'float':        TokenEnum.KWFloat,
        'for':          TokenEnum.KWFor,
        'goto':         TokenEnum.KWGoto,
        'if':           TokenEnum.KWIf,
        'int':          TokenEnum.KWInt,
        'malloc':       TokenEnum.KWMalloc,
        'NULL':         TokenEnum.KWNull,
        'random_alloc': TokenEnum.KWRandomAlloc,
        'return':       TokenEnum.KWReturn,
        'sizeof':       TokenEnum.KWSizeof,
        'struct':       TokenEnum.KWStruct,
        'true':         TokenEnum.KWTrue,
        'typedef':      TokenEnum.KWTypedef,
        'void':         TokenEnum.KWVoid,
        'while':        TokenEnum.KWWhile,
}
