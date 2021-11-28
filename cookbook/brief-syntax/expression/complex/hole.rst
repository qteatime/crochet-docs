Holes
=====

A hole (``_``) can occurr in applications or invocations. Doing so results
in a partially evaluated, delayed program.

For applications, it has the following syntax (here we have a delayed program
with two parameters)::

    Some-expression(A, _, B, _, C)

For invocations, it has the following syntax (here we have a delayed program
with one parameter)::

    _ between: 1 and: 5

These delayed programs can be applied later as normal::

    let Program = _ between: 1 and: 5;
    Program(3);
    // Equivalent to `3 between: 1 and: 5`