from rply import ParserGenerator
from AST import Number, Sum, Sub, Mul, Div, Smaller, Greater, Noteq, Equal, SmallerEq, GreaterEq, Print
from AST import *

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'STRINGV', 'REALV', 'BOOLV',
            'PROGRAM', 'IF', 'ELSE', 'THEN', 'DO', 'WHILE', 'END', 'PRINT',
            'AND', 'OR', 'INT', 'STRING', 'REAL', 'BOOL', 
            # 'TRUE', 'FALSE', 
            'FOR', 'MAIN',
            'PLUS', 'MINUS', 'MULT', 'DIV',
            'IDENTIFIER',
            'SMALLERTHAN', 'GREATERTHAN', 'NOTEQ', 'EQUAL', 'SMALLEREQ', 'GREATEREQ',
            'OPAREN', 'CPAREN', 'HASHTAG', 'OBRACKET', 'CBRACKET', 'COLON', 'SEMICOLON',
            'DOT', 'QUOTE', 'COMMA', 'ASSIGN', 'NEWLINE'
            ],
            precedence = [
                ('left', ['OR']),
                ('left', ['AND']),
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV'])
            ]
        )

    def parse(self):
        #   PRINT program
        @self.pg.production('program : PROGRAM MAIN expression END PROGRAM MAIN')
        def program(p):
            return Print(p[2])

        #   DATATYPES
        @self.pg.production('expression : REALV')
        def expression_realv(p):
            # p is a list of the pieces matched by the right hand side of the rule
            return Real(float(p[0].getstr()))
        
        @self.pg.production('expression : NUMBER')
        def expression_number(p):
            # p is a list of the pieces matched by the right hand side of the rule
            return Number(int(p[0].getstr()))
        
        @self.pg.production('expression : STRINGV')
        def expression_stringv(p):
            return String(p[0].getstr())
        
        @self.pg.production('expression : BOOLV')
        def expression_boolv(p):
            return Bool(p[0].getstr())  # process everything as true
        
        #   TYPES
        @self.pg.production('type : INT')
        @self.pg.production('type : STRING')
        @self.pg.production('type : REAL')
        @self.pg.production('type : BOOL')
        def type(p):
            return p[0].getstr()
        
        #   NESTED EXPRESSION W PARENTHESIS
        @self.pg.production('expression : OPAREN expression CPAREN')
        def expression_nested(p):
            return p[1]
        
        #   DECLARATION NONE (STATEMENT)
        @self.pg.production('expression : type COLON COLON moreIdentifiers')        
        def declaration_none(p):
            # print("Production Declaration")
            listids = p[3]
            for x in listids:
                print("id: " + x)
                Declare(p[0], x).eval()
                print("Parser declared")
                print(sytab.dict.values())
            return
        
        #   LIST OF IDENTIFIERS
        @self.pg.production('moreIdentifiers : IDENTIFIER COMMA moreIdentifiers')
        def moreIdentifiers(p):
            return([p[0].getstr()] + p[2])    #   TypeError: unsupported operand type(s) for +: 'Identifier' and 'list'
        
        #   ATOMIC IDENTIFIER
        @self.pg.production('moreIdentifiers : IDENTIFIER')
        def atomic_identifier(p):
            return([p[0].getstr()])
        
        #   DECLARATION AND ASSIGNMENT
        @self.pg.production('expression : type COLON COLON IDENTIFIER right_assignment')
        def declare_and_assign(p):
            Declare(p[0], p[3]) #   First delclares, then assigns on symbolTable
            return Assign(p[3], p[4]) #p[3] 
        
        #   ASSIGNMENTS
        @self.pg.production('right_assignment : ASSIGN expression')  #needed to maintain left
        def right_assignment(p):
            return(p[1])
        
        #   ARITHMETIC PROGRAMS
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

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
    
"""
Manejar la traducción de expresiones booleanas par las proposiciones if-then
mediante flujo del control, es decir si E1 or E2, donde E1 es verdedero, no 
llegar a evaluar E2.
"""