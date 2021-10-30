from pygments.lexer import RegexLexer, include, words
from pygments.token import *

keywords = [
  "relation",
  "predicate",
  "when",
  "do",
  "command",
  "action",
  "type",
  "enum",
  "define",
  "singleton",
  "goto",
  "call",
  "let",
  "return",
  "fact",
  "forget",
  "new",
  "search",
  "if",
  "simulate",
  "true",
  "false",
  "not",
  "and",
  "or",
  "is",
  "self",
  "as",
  "event",
  "quiescence",
  "for",
  "until",
  "in",
  "foreign",
  "on",
  "always",
  "match",
  "then",
  "else",
  "condition",
  "end",
  "with",
  "prelude",
  "rank",
  "tags",
  "abstract",
  "lazy",
  "force",
  "context",
  "sample",
  "of",
  "open",
  "local",
  "test",
  "assert",
  "requires",
  "ensures",
  "handle",
  "effect",
  "continue",
  "perform",
  "dsl",
  "has",
  "trait",
  "implement",
  "public",
  "capability",
  "protect",
  "global",
  "otherwise",
  "true",
  "false",
  "nothing"
]

class CrochetLexer(RegexLexer):
  name = 'Crochet'
  aliases = ['crochet']
  filenames = ['*.crochet']

  tokens = {
    'root': [
      (r'%[ \t]*crochet/', Comment.Single),
      include('common')
    ],

    'common': [
      (r'(?<![a-zA-Z0-9\-])([A-Z][a-zA-Z0-9\-]*|_)', Name.Variable),
      (r'(?<![a-zA-Z0-9\-])([a-z][a-zA-Z0-9\-]*)(:)', Name.Function),
      (words(keywords, prefix=r'(?<![a-zA-Z0-9\-\.\'#])', suffix=r'(?![a-zA-Z:\.\-])'), Keyword),
      (r'([a-z][a-z0-9\.\-]*)', Text),
      (r'//.*', Comment.Single),
      (r'([\-\+]?[0-9][0-9_]*(?:\.[0-9][0-9_]*)?(?:[eE][\-\+]?[0-9][0-9_]*)?)', Number.Float),
      (r'([\-\+]?[0-9][0-9_]*)', Number.Integer),
      (r'\->|=>|<\-|===|=/=|>=|>|<=|<|\+\+|\+|\-|\*\*|\*|/|%|#', Operator),
      (r'[\(\)\[\]\{\};,:\|=\'\.]', Punctuation),
      (r'"', String.Delimiter, 'string_double'),
      (r'\s+', Text)
    ],

    'string_double': [
      (r'[^\\"\[]+', String.Double),
      (r'\[', String.Interpol, 'string_interpolation'),
      (r'\\(u[0-9a-fA-F]{4}|x[0-9a-fA-F]{2}|.)', String.Escape),
      (r'\\.', Error),
      (r'"', String.Delimiter, '#pop')
    ],

    'string_interpolation': [
      (r'\]', String.Interpol, '#pop'),
      include('common')
    ]
  }
