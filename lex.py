import ply.lex as lex

reserved = (
    'INT', 'FLOAT', 'IF', 'ELSE'
)

tokens = reserved + (
    # Literals
    'ID', 'INT_VAL', 'FLOAT_VAL',
    # Arithmetic ops
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    # Boolean
    'OR', 'AND', 'NOT',
    # Comparison
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    # Delimeters
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LCURLY', 'RCURLY',
    # Assignment
    'EQUALS',
    # Rest
    'COMMA', 'SEMI',
)

# ignore whitespace
t_ignore = ' \t'


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# Ops
# Arithmetic
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
# Boolean
t_OR = r'\|'
t_AND = r'&&'
t_NOT = r'!'
# Comparison
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
# Delimeters
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
# Assignment
t_EQUALS = r'='
# Rest
t_COMMA = r','
t_SEMI = r';'


reserved_keywords = {word.lower(): word
                     for word in reserved}


def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_keywords.get(t.value, 'ID')
    return t


def t_FLOAT_VAL(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t


def t_INT_VAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_comment(t):
    r' /\*(.|\n)*?\*/'
    t.lineno += t.value.count('\n')


def t_error(t):
    print('Illegal characted %s'.format(repr(t.value[0])))


lexer = lex.lex()


if __name__ == '__main__':
    lex.runmain(lexer)
