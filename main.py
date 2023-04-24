from Lexer import Lexer
from Parser import Parser

# text_input = """
# print(4 + (5 * 2))
# """

text_input = """
print(2*1)
"""

lexer = Lexer().get_lexer()
pg = Parser()

tokens = lexer.lex(text_input)

# for token in tokens:
#     print(token)

pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()