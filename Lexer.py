from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()
    def _add_tokens(self):
        # data types
        self.lexer.add('REALV', r'\d+\.\d+')
        self.lexer.add('NUMBER', r'\d+')
        self.lexer.add('STRINGV', r'\".*\"')
        
        # reserved words (keywords)
        self.lexer.add('PROGRAM', r'program')
        self.lexer.add('IF', r'if')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('THEN', r'then')
        self.lexer.add('DO', r'do')
        self.lexer.add('WHILE', r'while')
        self.lexer.add('END', r'end')
        self.lexer.add('PRINT', r'print')
        self.lexer.add('AND', r'and')
        self.lexer.add('OR', r'or')
        self.lexer.add('INT', r'int')
        self.lexer.add('STRING', r'string')
        self.lexer.add('REAL', r'real') #float
        self.lexer.add('BOOL', r'bool')
        self.lexer.add('TRUE', r'true')
        self.lexer.add('FALSE', r'false')
        self.lexer.add('FOR', r'for')
        self.lexer.add('MAIN', r'main')
        
        # VARIABLE
        self.lexer.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')

        # arithmetic operators
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('MINUS', r'-')
        self.lexer.add('MULT', r'\*')
        self.lexer.add('DIV', r'/')

        # relational operators
        self.lexer.add('NOTEQ', r'!=')
        self.lexer.add('EQUAL', r'==')
        self.lexer.add('SMALLEREQ', r'<=')
        self.lexer.add('GREATEREQ', r'>=')
        self.lexer.add('SMALLERTHAN', r'<')
        self.lexer.add('GREATERTHAN', r'>')

        # parenthesis and extras
        self.lexer.add('OPAREN', r'\(')
        self.lexer.add('CPAREN', r'\)')
        self.lexer.add('HASHTAG', r'#')
        self.lexer.add('OBRACKET', r'{')
        self.lexer.add('CBRACKET', r'}')
        self.lexer.add('COLON', r':')
        self.lexer.add('SEMICOLON', r';')
        self.lexer.add('DOT', r'\.')
        self.lexer.add('QUOTE', r'"')
        self.lexer.add('COMMA', r',')
        self.lexer.add('ASSIGN', r'=')
        self.lexer.add('NEWLINE', r'\\n')
        
        # ignore spaces
        self.lexer.ignore('\s+')
    
    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()

