Delayed programs (Lambdas)
==========================

A delayed program (or lambda) is a program that needs to be applied
in order to be executed.

A delayed program with no parameters is constructed through the
following syntax::

    { Some-expression }

A delayed program with parameters is constructed through the
following syntax (where ``A``, ``B``, and ``C`` are its parameters)::

    { A, B, C in
      Some-expression
    }
