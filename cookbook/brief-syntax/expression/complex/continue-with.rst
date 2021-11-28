``continue with`` expression
============================

The continue with expression is used within an effect handler
to transfer the execution back to its continuation---the ``perform``
instruction that caused it to run. It has the following syntax::

    continue with Some-expression;