from Juliet_DB_loader import TestCase, Folder, SubFolder, sessionmaker, engine

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

from ply import lex, yacc

tokens = ['COMMENT', 'CODE']

# Define lexer rules
def t_COMMENT(t):
    r'/\*(.|\n)*?\*/|//.*'
    lines = t.value.split('\n')
    t.lexer.lineno += len(lines) - 1
    
def t_CODE(t):
    r'[^\n]+'  # Match any characters that are not newline
    t.lexer.lineno += max(1, t.value.count('\n'))  # Ensure at least one line for an empty string
    return t

# Add a separate rule for empty lines
def t_EMPTYLINE(t):
    r'^\s+$'
    t.type = 'CODE'  # Change token type to 'CODE'
    return t

#TO-DO Separate Rules for In-Line Comments and Block Comments


# Ignore whitespace
t_ignore = ' \t'
# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Define parser rules
def p_code(p):
    '''code : code COMMENT
            | code CODE
            | COMMENT
            | CODE'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]

def p_error(p):
    pass

lexer = lex.lex()

parser = yacc.yacc(write_tables=False)

# This is the function that will be used to strip comments from the code
def strip_comments_and_preserve_line_numbers(code_lines):
    stripped_lines = []
    lexer.input('\n'.join(code_lines))  # Feed the entire code to the lexer
    for token in lexer:
        if token.type == 'COMMENT':
            stripped_lines.append('\n' * token.value.count('\n'))  # Replace comment with newlines
        elif token.type == 'CODE':
            stripped_lines.append(token.value)    
    return stripped_lines

# Example usage
c_code = session.query(TestCase).filter_by(id=1000).first()
# Then split this into lines

c_code_content = c_code.file_content.split('\n')

# Strip comments and preserve line numbers
stripped_lines = strip_comments_and_preserve_line_numbers(c_code_content)

# Print each line number and line content on a separate line
for line_number, line_content in enumerate(stripped_lines, start=1):
    print(f"{line_number}: {line_content}")


