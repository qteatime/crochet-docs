from sphinx.highlighting import lexers
from .crochet_lexer import *

def setup(app):
  lexers['crochet'] = CrochetLexer()