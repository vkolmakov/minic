name_with_pattern = [
    ('IF', r'if'),
    ('ELSE', r'else'),
    ('INT_TYPE', r'int'),
    ('FLOAT_TYPE', r'float'),

    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\['),
    ('RBRACE', r'\]'),
    ('LCURLY', r'\{'),
    ('RCURLY', r'\}'),

    ('NOT_EQUAL', r'!='),
    ('EQUAL_EQUAL', r'=='),
    ('GREATER', r'>'),
    ('GREATER_EQUAL', r'>='),
    ('SMALLER', r'<'),
    ('SMALLER_EQUAL', r'<='),

    ('FLOAT', r'\d+\.\d*'),
    ('INTEGER', r'\d+'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),

    ('AND', r'\&\&'),
    ('OR', r'\|\|'),

    ('BANG', r'!'),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('MUL', r'\*'),
    ('DIV', r'\/'),
    ('MOD', r'\%'),

    ('SEMI', r';'),
    ('COMMA', r','),
    ('EQUAL', r'='),
]

names = [name for (name, _) in name_with_pattern]
