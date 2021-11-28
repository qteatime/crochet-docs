Using data
==========

Literal data
------------

Most basic pieces of data have a "literal" form in Crochet. These are used
to construct basic values in the language. Crochet supports the following
literal forms:

- **Integers**: things like ``1``, ``-300``, and ``1_200_300``
  (underscores can be used as a separator for thousands).

- **Fractional (Floats)**: things like ``1.0``, ``-300.34``, and ``1_200_300.456``.

- **Text**: things like ``"Hello"`` or ``<<The cat sleeps>>``.

- **Interpolations**: things like ``"Hello, [Name]"`` or ``<<Hello, [Name]>>``.

- **Booleans**: either ``true`` or ``false``.

- **Nothing**: ``nothing``.

- **Lists**: things like ``[]`` or ``[1, 2, 3, 4]``.

- **Records**: things like ``[->]`` or ``[name -> "Alice", appears-in -> "Alice in Wonderland"]``.

Each of these is described in more details in their respective section in
the Intrinsic data types chapter.


.. _new-operator:

The ``new`` operator
--------------------

In order to manipulate most complex pieces of data in Crochet they have to
be :ref:`typed <type-declaration>`. And we bring typed data into existence
with the ``new`` operator::

    // Given the type
    type point2d(x, y);

    // We can construct it
    new point2d(1, 2);

Here, ``x`` and ``y`` are :ref:`fields <typed-fields>` of the type
``point2d``, and the ``new`` operator binds values to those fields. Hence,
``x`` will be bound to ``1``, and ``y`` bound to ``2``.

The syntax for the ``new`` operator is similar to that of the type 
declaration, but we put data where the field specifications would go. In
this sense, we call the ``new`` operator :term:`positional <positional argument>`.
That is, we don't explicitly tell Crochet which values will be bound to which
fields, but rather that association is done based on the position
that the data and field specifications have in the list.

Here the field ``x`` is the first one in the type declaration, and the field
``y`` is the second one. That's why the first piece of data, ``1`` gets bound
to ``x``.


Constructing capabilities
'''''''''''''''''''''''''

Because Crochet uses types for capabilities, there are restrictions on
*who* can construct typed data through the ``new`` operator. So one can
only use the :ref:`new operator <new-operator>` directly if the type
being constructed is defined in the same package as the calling code.

That is, if one were to define a type ``point2d`` in package A, then
try to construct it in package B, the runtime will prevent this action
because B does not have direct constructing capabilities over types
defined by A. This gives A control over which capabilities it wants
to provide, and how it wants to provide those capabilities.

Capabilities and how exactly Crochet achieves its safety guarantees
is discussed in more details in the Security and Capabilities section.

.. _field-projection:

Projecting fields
-----------------

So typed data consists of several named pieces of data. In order to use a
particular piece of data, we need to project it out. This is done by using
the ``.`` (dot) operator.

Given a type such as the following::

    type point2d(x, y);

And a typed data construct like::

    let P = new point2d(1, 2);

Then we can project fields out of it::

    P.x; // ==> 1


Non-existing fields
'''''''''''''''''''

Trying to project a field that does not exist in a typed data is an error,
but this error may not be reported until Crochet tries to execute that
projection. For example::

    type point2d(x, y);

    let P = new point2d(1, 2);
    P.z;
    // *** Error: The type point2d does not have a field `z`
    //            (known fields: [x, y])


Fields and inheritance
''''''''''''''''''''''

Types can be described in a hierarchy. Thus, if we have something like::

    type point2d(x, y);
    type point3d(a, b, c) is point2d;

Then ``point3d`` can be provided both where ``point2d`` and ``point3d`` are
expected. This poses a problem with field projection because ``x`` and ``y``
are fields in ``point2d``, but they are not fields in ``point3d``. Types
do not inherit any data layout from their supertypes in Crochet. This means
that the following would cause very confusing failures::

    command point2d x = self.x;

    let P = new point3d(1, 2, 3);
    P x;
    // *** Error: The type point3d does not have a field `x`
    //            (known fields: [a, b, c])
    //
    //     Arising from:
    //       In (point2d) x
    //         from module (repl) in crochet.repl.basic

For this reason, any command that is meant to be shared with other types
should not use field projection directly, but rather rely on commands whose
only job is to project that field, so the commands can be defined for the
types that need it.


Visibility of fields
''''''''''''''''''''

Allowing code to project fields from typed data is a dangerous kind of
power. If typed data is to be used for privacy, then arbitrary projection
could very well violate that guarantee, since it's not necessary to know
the type in order to perform a projection.

To address this, projection of typed data is only possible within the
package that defines the type. This means that any access to the
information inside of a typed data is conditioned to commands instead,
and these follow the expected Crochet guarantees. Users can decide which of
the fields in a typed data can safely be exposed as commands, and what kind
of capabilities are necessary in order to access them.


Projection with non-typed data
------------------------------

Projection is not restricted to typed data in Crochet. It's also available
on sequences and records, and it does slightly different things with them.


Record projection
'''''''''''''''''

Records are non-typed pieces of data comprised of independent information.
For example, one could represent coordinates as records like so::

    let Coords = [latitude -> -75.0, longitude -> 31.0];

And these pieces of information can be projected like in a typed data::

    Coords.latitude; // ==> -75.0

Projecting non-existing fields will, likewise, result in an error::

    Coords.lat;
    // *** Error: The key `lat` does not exist in the record
    //            (known keys: latitude, longitude)

.. danger::

   Since records are not typed, they cannot provide any privacy or security
   guarantees and should not be used for data that isn't completely public.


Sequence projection
'''''''''''''''''''

.. warning::

   This is an experimental feature and it's likely to change!

Using projection on a sequence, like ``[A, B, C].x`` is equivalent to
projecting each item of the sequence, so the result will be
``[A.x, B.x, C.x]``.

For example, given::

    let Alice = [name -> "Alice", author -> "Lewis Caroll"];
    let Dorothy = [name -> "Dorothy", author -> "L. Frank Baum"];

    let Characters = [Alice, Dorothy];

If we project the ``name`` field of this sequence, that's equivalent to
projecting the ``name`` field of each record::

    Characters.name; // ==> ["Alice", "Dorothy"]

