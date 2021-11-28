Pipe expressions
================

A pipe expression allows some parenthesis to be omitted by expressing
sequences of command executions as a pipeline. It has two forms, and
they may not be mixed.


Self pipe
---------

The self pipe (``|``) allows the result of a previous expression to be
passed as the ``self`` parameter to another command. It has the
following syntax::

    Some-expression
      | some-command: Args may: Go here: Too
      | more-commands
      | yet-more-commands: Go-here

Only a single postfix or a single keyword command is allowed after the
pipe. And the above is roughly equivalent to the following::

    let A = Some-expression;
    let B = A some-command: Args may: Go here: Too;
    let C = B more-commands;
    let D = C yet-more-commands: Go-here;


Generic pipe
------------

The generic pipe (``|>``) allows the result of a previous expression to
be provided to an unary delayed program. It has the following syntax::

    Some-expression
      |> _ some-command: Args may: Go here: Too
      |> { A in A more-commands }
      |> yet-more-commands: _;

The expression to the right of a generic pipe should always be a delayed
program that takes one argument. The above is roughly equivalent to the
following::

    let A = Some-expression;
    let B = (_ some-command: Args may: Go here: Too)(A);
    let C = ({ A in A more-commands })(B);
    let D = (yet-more-commands: _)(C);
