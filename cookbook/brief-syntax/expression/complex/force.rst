``force`` expression
====================

A force expression takes in a Lazy delayed program and executes it,
if it hasn't been executed before, to get its value. It has the
following syntax::

    force Some-expression;