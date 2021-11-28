``perform`` expression
======================

A perform expression raises the intention for an effect to occurr,
allowing Crochet to search for a handler to it to be executed.
It has the following syntax::

    perform some-effect.operation(
      Argument-1,
      Argument-2,
    )

Trailing commas are allowed in the list of arguments, but not required.