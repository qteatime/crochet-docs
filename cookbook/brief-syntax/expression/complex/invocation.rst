Command invocation
==================

A global command may be invoked with a syntax that is similar to how
it is declared. Thus the following forms exist:


Postfix invocation
------------------

A postfix ``_ some-command-name`` command is invoked with::

    Some-expression some-command-name


Prefix invocation
-----------------

A prefix ``not _`` command is invoked with::

    not Some-expression


Binary invocation
-----------------

A binary ``_ + _`` command is invoked with::

    Some-expression + Other-expression


Keyword invocation
------------------

A keyword ``_ and: _ then: _`` command is invoked with::

    Some-expression
      and: Other-expression
      then: Another-expression

Self-less keyword invocation
----------------------------

A self-less keyword ``and: _ then: _`` command is invoked with::

    and: Some-expression then: Other-expression


Precedence rules
----------------

Crochet's precedence rules are based more on the syntax of the
command than on specific names. However, a few binary names are
special. In the following list, expressions further down in the list
can be included in the holes of expressions above it without parenthesis:

- ``Postfix <- Pipe`` (binary, store)
- ``Binary and: Binary then: Binary`` (keyword)
- ``Prefix === Prefix``, ``Prefix as Type`` (binary, others)
- ``not Postfix`` (prefix)
- ``Simpler-expression some-name`` (postfix)


Associativity rules
-------------------

Crochet requires explicit parenthesis for binary invocations by default.
A convenience exception is made for binary commands that are associative
as long as the sequence only includes that command. E.g. the following
does not require parenthesis::

    1 + 2 + 3 + 4

But the following does::

    1 + 2 + (3 - 4)


Partial invocation
------------------

Any argument to a command can be the special hole (``_``) syntax,
in which case the command is only partially applied, resulting in
a partial program that can be, later on, further applied to other
arguments.

It has the following syntax::

    _ between: 1 and: 5
