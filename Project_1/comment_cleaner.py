from Juliet_DB_loader import TestCase, Folder, SubFolder, sessionmaker, engine

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

from ply import lex, yacc

# Define Tokens
tokens = ['INLINE_COMMENT', 'MULTILINE_COMMENT', 'NEWLINE', 'CODE', 'ERROR_CODE']

# Define lexer rules

def t_MULTILINE_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    lines = t.value.split('\n')
    t.lexer.lineno += len(lines) - 1
    return t
def t_INLINE_COMMENT(t):
    r'(/\*.*?\*/)|(//.*)'
    t.lexer.lineno += 1
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_CODE(t):
    r'[^\n]+'  # Match any characters that are not newline
    t.lexer.lineno += max(1, t.value.count('\n'))  # Ensure at least one line for a non-empty string
    if not t.value.strip():
        t.type = 'ERROR_CODE'  # Change token type to 'ERROR_CODE'
        t.value = '0'  # Placeholder value
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)
# Define parser rules
def p_code(p):
    '''code : INLINE_COMMENT
            | MULTILINE_COMMENT
            | NEWLINE
            | CODE
            | ERROR_CODE'''

def p_code(p):
    '''code : line
            | comment
            | NEWLINE
            | ERROR_CODE'''

def p_line(p):
    '''line : CODE NEWLINE
            | CODE'''

def p_comment(p):
    '''comment : INLINE_COMMENT NEWLINE
               | MULTILINE_COMMENT NEWLINE
               | INLINE_COMMENT
               | MULTILINE_COMMENT'''
    

def p_error(p):
    print("Syntax error at '%s'" % p.value)

lexer = lex.lex()

parser = yacc.yacc(write_tables=False, debug = True)

# This is the function that will be used to strip comments from the code
def strip(code_lines):
    stripped_lines = []
    token_counts = {'MULTILINE_COMMENT': 0, 'INLINE_COMMENT': 0, 'NEWLINE': 0, 'CODE': 0, 'ERROR_CODE': 0, }
    token_lines = {'MULTILINE_COMMENT': [], 'INLINE_COMMENT': [], 'NEWLINE': [], 'CODE': [], 'ERROR_CODE': []}
    lexer.input('\n'.join(code_lines))  
    last_token = None
    tokens = list(lexer)
    for i, token in enumerate(tokens):
        token_counts[token.type] += 1
        token_lines[token.type].append(token.lineno)
        next_token = tokens[i + 1] if i + 1 < len(tokens) else None

        if token.type == 'MULTILINE_COMMENT':
            stripped_lines.extend([''] * token.value.count('\n'))
        elif token.type == 'INLINE_COMMENT':
            # Remove inline comment
            pass
        elif token.type == 'NEWLINE':
            # Conditions for newline issue handling. 
            
            #1 Don't add newline if next token is a a code token.
            if last_token and last_token.type == 'CODE':
               pass
            else:
                stripped_lines.append('\n')  

        elif token.type == 'CODE':
            # Preserve lines of code
            stripped_lines.append(token.value)
        elif token.type == 'ERROR_CODE':
            stripped_lines.appent('X')    
        last_token = token  # Update last_token
        
    return stripped_lines, token_counts, token_lines


# Example usage
c_code = session.query(TestCase).filter_by(id=1000).first()
# Then split this into lines

c_code_content = c_code.file_content.split('\n')

# Strip comments and preserve line numbers
stripped_lines, token_counts, token_lines = strip(c_code_content)

#Print each line number and line content on a separate line
for line_number, line_content in enumerate(stripped_lines, start=1):
    print(f"{line_number}: {line_content}")

# Print token counts and lines where they occur
for token_type in token_counts:
    print(f"{token_type}: {token_counts[token_type]} occurrences")
    print(f"Lines where {token_type} occurs: {token_lines[token_type]}")

for code_line in token_lines['CODE']:
    if code_line in token_lines['MULTILINE_COMMENT'] or code_line in token_lines['INLINE_COMMENT']:
        print(f"Line {code_line} contains both code and comment.")
    # else:
    #     print(f"Line {code_line} contains code only.")
