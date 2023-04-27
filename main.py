from Lexer import Lexer
from Parser import Parser
# import os

# print("Current working directory:", os.getcwd())
f = open("micompa/input.hppy", "r")
text_input = f.read()

translate = {}
for line in open('micompa/Translator/rosettaStone.txt'):
        fortran, hoppy = line.split(',')
        text_input = text_input.replace(str(fortran), str(hoppy[:-1]))  #   [:-1] is for avoiding '/n'
        translate[fortran] = hoppy[:-1] #   not used by the moment

# Write the file out again
with open('micompa/Translator/input_hoppy.txt', 'w') as file:
  file.write(text_input)


lexer = Lexer().get_lexer()
pg = Parser()

tokens = lexer.lex(text_input)

# #   NEED TO RUN EITHER THIS BLOCK OR THE PARSING ONE
# for token in tokens:
#     print(token)

pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()