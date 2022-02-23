``type``
========

A type declaration introduces a type in Crochet, it has multiple forms.
Types always accept a preceding documentation comment.


Foreign types
-------------

Foreign types allow types defined by native modules to be used by
Crochet modules. It's currently restricted to modules in the standard
library. It has the following syntax::

    type some-name = foreign some.type.name;


Enumeration types
-----------------

Enumeration types define a set of singleton types that are closed and
have an intrinsic ordering. It has the following syntax::

    enum some-name =
      first-value,
      second-value,
      third-value;

It is roughly equivalent to the following, more verbose definition, along
with a handful of pre-defined commands::

    abstract some-name;
    singleton some-name--first-value is some-name;
    singleton some-name--second-value is some-name;
    singleton some-name--third-value is some-name;

Enumeration types do not support inheriting from another type.


Abstract types
--------------

An abstract type is a type that cannot be constructed by Crochet code. It
has the following syntax::

    abstract some-name;

It may inherit from another type::

    abstract some-name is some-other-type;


Singleton types
---------------

A singleton type is a type that has one global object pre-defined, and
does not allow new objects to be constructed. It has the following syntax::

    singleton some-name;

It may inherit from another type::

    singleton some-name is some-other-type;

It is roughly equivalent to the following, more verbose definition (with
the caveat the ``seal`` is an internal operation)::

    type some-name;
    define some-name = new some-name;
    seal some-name;


Convenience commands
''''''''''''''''''''

Singleton types offer a syntax that is similar to what may be found in
other object-oriented languages for the definition of commands that
"belong" to the type. It has the following syntax::

    singleton some-name with
      command postfix-command = Expression;
      command and: _ then: _ = Expression;
    end

And it is roughly equivalent to the following, more verbose definition::

    singleton some-name;

    command some-name postfix-command = Expression;
    command some-name and: _ then: _ = Expression;

Only post-fix and keyword commands are supported in this convenience form.


Regular types
-------------

With no parameters
''''''''''''''''''

A regular type with no parameters has the following syntax::

    type some-name;

Such types can inherit from others through the following syntax::

    type some-name is some-other-type;


With parameters
'''''''''''''''

A regular type with parameters has the following syntax::

    type some-name(
      first is some-constraint,
      second is other-constraint,
    );

A trailing comma in the list of parameters is allowed.

Such types can inherit from others through the following syntax::

    type some-name(
      first is some-constraint,
      second is other-constraint,
    ) is some-other-type;

Parameter constraints are the same as Commands Requirements.