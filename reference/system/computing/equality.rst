Equality
========

When are two Crochet values equal? This question is surprisingly
difficult to answer, and in this section we cover the common 
cases that give one an idea of how to think about equality.


Intrinsic equality
------------------

Every value in Crochet has a concept of "intrinsic equality".
That is, within the Crochet universe, what other value is
equal to it. In this case, the idea of intrinsic equality
means that, if two values are intrinsically equal, then
they can be used interchangeably anywhere in Crochet.
In any context.

Intrinsic equality is computed through the intrinsic
equality operator (``=:=``, two equal signs separated by a double colon symbol).
This is not really a Crochet command, but a special piece of Crochet
syntax that has a well-defined, immutable meaning.

In essence, in an expression like ``A =:= B``, we consider ``A`` and ``B``
equal if:

- They are both integers, and represent the same number;

- They are both floating points, and represent the same number. This still
  holds for infinities (positive infinity is equal to any other positive
  infinity representation, for example), but it does not hold for the
  special "not a number" (NaN) representation. That's because NaN is never
  equal to anything---it is the representation of a numeric error.

- They are both text, and their normalised unicode representation is
  the same. What a "normalised unicode representation" is is explained
  in the Text models chapter.

- They are both booleans, and both are the value ``true``, or both are
  the value ``false``.

- They are both ``nothing``.

- They are both interpolations, and the order and values of their textual
  and dynamic parts are equal to each other. That is, ``"Hello, [Name]"``
  is equal to ``"Hello, [Person]"`` if ``Name`` and ``Person`` are equal,
  but ``"[Greeting], Alice"`` and ``"Hello, [Name]"`` can never be equal,
  even if ``Greeting`` is the text ``"Hello"`` and ``Name`` is the text
  ``"Alice"``, thus being displayed to the user as "Hello, Alice".

- They are both lists, and they contain the same number of values, and
  each value in one list is intrinsically equal to the value at the 
  same position in the other list. ``[1, 2, 3]`` and ``[1, 2, 3]`` are
  equal, ``[1, 2, 3]`` and ``[3, 2, 1]`` are not.

- They are both records, and they contain the same set of keys, which
  are associated with equal values. ``[x -> 1, y -> 2]`` and ``[y -> 2, x -> 1]``
  are equal, but ``[x -> 1, y -> 2]`` and ``[x -> 1, z -> 2]`` are not.

All other values in Crochet are considered intrinsically equal if their
identities are the same.


Value identity
--------------

Typed data is brought into existence through the ``new`` operator. When
this happens, Crochet assigns an unique identity to the value. Like
a social security number uniquely identifying a person---but this applies
everywhere in Crochet.

That is, if we have::

    let A = new point2d(1, 2);
    let B = new point2d(1, 2);

Then ``A`` and ``B`` have distinct (and unique) identities, even though
they may contain the same values. This is important for Crochet's idea
of security---it allows each of these values to be used as a completely
unique key, allowing whoever controls these values to also control access
to other things.

For example, the ``map`` type in Crochet uses intrinsic equality to
associate arbitrary keys with values. This means that if we have the
following::

    let Map = #map empty
                | use-strict-access
                | at: A put: "Hello"
                | at: B put: "Goodbye";

And we give ``A`` and ``B`` to other people, then people who have
got ``A`` will only ever be able to get ``"Hello"`` out of this map.
And people who have got ``B`` will only ever be able to get ``"Goodbye"``
out of it.


Custom equality
---------------

The standard library also describes an ``equality`` trait, which proposes
that typed data may define its own notion of equality, where desirable.
Thus, the ``_ === _`` (equals) command is only defined for some types,
and what it means is up to the people implementing the trait.

For example, if we were to make a ``rectangle`` type, it would be useful
to also allow people to compare them for equality. And since rectangles
don't usually carry any sensitive data, we don't have to worry as much
about security in this case.

This definition could look like this::

    type rectangle(global width, global height);

    implement equality for rectangle;

    command (A is rectangle) === (B is rectangle) =
      (A width === B width) and (A height === B height);

So, in this case, rectangles would be equal if they have the same width
and height. Note, however, that due to how types in Crochet are laid out
in a hierarchy, it is still possible for users to extend this rectangle
type and still have this same equality notion apply to them.

Consider the following::

    type square(global side) is rectangle;

    command square width = self side;
    command square height = self side;

With this definition, the following would all be equal (through ``_ === _``)
to each other, even though different *types* are involved::

    let A = new rectangle(10, 10);

    let B = new rectangle(10, 10);

    let C = new square(10);

    (A === B) and (B === C);


Security considerations
'''''''''''''''''''''''

When making types implement equality, you need to ensure that it makes
sense from a security point of view as well, if your type may contain
sensitive data, or be used for sensitive operations.

By implementing custom equality you're choosing to make some aspect of
your value observable and comparable to other values in Crochet.
Every time you choose to make some aspect of your data observable,
you may end also giving others a way of guessing sensitive data.
Or, if equality only considers a value partially, you may end up
in situations where people are able to perform things in your
program even though they should not have the permission to do so.