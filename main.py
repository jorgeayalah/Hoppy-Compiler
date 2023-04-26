from Lexer import Lexer
from Parser import Parser
# import os

# print("Current working directory:", os.getcwd())
f = open("micompa/input.beer", "r")
text_input = f.read()

lexer = Lexer().get_lexer()
pg = Parser()

tokens = lexer.lex(text_input)

# #   NEED TO RUN EITHER THIS BLOCK OR THE PARSING ONE
# for token in tokens:
#     print(token)

pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()
# print()