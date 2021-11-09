Program representations
=======================

Crochet differentiates delayed programs created through the ``lazy``
special syntax and other partial or delayed programs created either
through holes or the curly-brackets syntax. The primary reason for
this is that they really do behave differently under the hood, and
unifying them would make things more confusing.


Thunks
------

A lazy delayed program (created through the ``lazy`` special syntax)
is a Thunk, and it's associated with the ``thunk`` type. The ``force``
special syntax, which executes a lazy delayed program if no value for
it has been computed before, is the primary way of interacting with
these programs.


Functions
---------

Every other delayed or partial program is a Function---a representation
of a (maybe partial) program that can be executed at will through the
``Program()`` syntax.

Functions are classified by the number of requirements they have. Also
called their "arity". For example, the function ``{ 1 + 2 }`` has no
requirements, and thus arity 0 (or nullary). It is represented by the
type ``function-0``. Whereas the function ``{ A, B in A + B }`` and
the function ``_ + _`` both have two requirements, and thus arity 2
(or binary). These are represented by the type ``function-2``.

Functions can be executed by providing values to all of their
requirements::

    let Add = { A, B in A + B };
    Add(1, 2);

It's not immediately obvious by looking at this syntax if all of
the requirements have been fulfilled, but for Crochet it's an error
if the number of values we provide differs from the number of
requirements.


Partials
''''''''

A Partial is a special kind of function that's created when commands
are partially applied. For example, the expression ``_ + 1`` creates
a value of the type ``partial-1``. Partials can be used anywhere
functions of the same arity are expected.