List expression
===============

The list expression constructs a list from a sequence of expressions.
If all expressions are atomic, then the list itself is also atomic.

The empty list has the following syntax::

    []

A list with items in it has the following syntax::

    [
      Some-expression,
      Other-expression,
      More-expressions,
    ]

The list of expressions may have a trailing comma, but it's not required.