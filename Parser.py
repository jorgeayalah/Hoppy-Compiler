from rply import ParserGenerator
from AST import Number, Sum, Sub, Mul, Div, Smaller, Greater, Noteq, Equal, SmallerEq, GreaterEq, Print
from AST import *


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'STRINGV', 'REALV',
            # 'IDENTIFIER',
            'PROGRAM', 'IF', 'ELSE', 'THEN', 'DO', 'WHILE', 'END', 'PRINT',
            'AND', 'OR', 'INT', 'STRING', 'REAL', 'BOOL', 'TRUE', 'FALSE', 'FOR', 'MAIN',
            'PLUS', 'MINUS', 'MULT', 'DIV',
            'SMALLERTHAN', 'GREATERTHAN', 'NOTEQ', 'EQUAL', 'SMALLEREQ', 'GREATEREQ',
            'OPAREN', 'CPAREN', 'HASHTAG', 'OBRACKET', 'CBRACKET', 'COLON', 'SEMICOLON',
            'DOT', 'QUOTE', 'COMMA', 'ASSIGN', 'NEWLINE'
            ],
            precedence = [
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV'])
            ]
        )

    def parse(self):
        # PRINT program
        @self.pg.production('program : PRINT OPAREN expression CPAREN')
        def program(p):
            return Print(p[2])

        #   DATATYPES
        @self.pg.production('expression : NUMBER')
        def expression_number(p):
            # p is a list of the pieces matched by the right hand side of the
            # rule
            return Number(int(p[0].getstr()))
        
        @self.pg.production('expression : STRINGV')
        def expression_stringv(p):
            return String(p[0].getstr())
        
        # NESTED EXPRESSION W PARENTHESIS
        @self.pg.production('expression : OPAREN expression CPAREN')
        def expression_nested(p):
            return p[1]
        
        # #   ASSIGNATION
        # @self.pg.production('expression : IDENTIFIER ASSIGN expression')
        # def expression_assign(p):
        #     return Assign(p[0], p[2])
        
        # ARITHMETIC PROGRAMS
        @self.pg.production('expression : expression PLUS expression')
        @self.pg.production('expression : expression MINUS expression')
        @self.pg.production('expression : expression MULT expression')
        @self.pg.production('expression : expression DIV expression')
        def expression_arith(p):
            left = p[0]
            right = p[2]
            operator = p[1]

            if operator.gettokentype() == 'PLUS':
                return Sum(left, right)
            elif operator.gettokentype() == 'MINUS':
                return Sub(left, right)
            elif operator.gettokentype() == 'MULT':
                return Mul(left, right)
            elif operator.gettokentype() == 'DIV':
                return Div(left, right)
            else:
                raise AssertionError('Oops, this aint a beer!')

        # RELATIONAL PROGRAMS
        @self.pg.production('expression : expression SMALLERTHAN expression')
        @self.pg.production('expression : expression GREATERTHAN expression')
        @self.pg.production('expression : expression NOTEQ expression')
        @self.pg.production('expression : expression EQUAL expression')
        @self.pg.production('expression : expression SMALLEREQ expression')
        @self.pg.production('expression : expression GREATEREQ expression')
        def expression_relational(p):
            left = p[0]
            right = p[2]
            operator = p[1]

            if operator.gettokentype() == 'SMALLERTHAN':
                return Smaller(left, right)
            elif operator.gettokentype() == 'GREATERTHAN':
                return Equal(left, right)
            elif operator.gettokentype() == 'NOTEQ':
                return Noteq(left, right)
            elif operator.gettokentype() == 'EQUAL':
                return Equal(left, right)
            elif operator.gettokentype() == 'SMALLEREQ':
                return SmallerEq(left, right)
            elif operator.gettokentype() == 'GREATEREQ':
                return GreaterEq(left, right)
            else:
                raise AssertionError('Oops, this aint a beer REL!')
        
        
        # @self.pg.production('expression : NUMBER')
        # def number(p):
        #     return Number(p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()