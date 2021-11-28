Collections
===========

Sometimes we need to deal with multiple values. Crochet has two primary
types for this: Lists and Records.


Lists
-----

A list is a sequence of similar items---where "similar" really means
"we can treat these uniformly", and often boils down to having the
same type.

Lists are written in the square brackets syntax::

    [1, 2, 3, 4, 5]

The expression above creates a list that contains 5 elements, which
are the integers from 1 to 5, in that exact order.

An empty list is written as follows::

    []

Lists can be peeked into, transformed, sorted, combined, and a so on.
The standard library defines a rich set of ways to manipulate lists,
and similar collections, such as sets.


Records
-------

A record is an unordered bag of values that can be referenced with
a key. Each key references exactly one value in a record, and all
values have a key.

We can write records using the bracket-with-arrows syntax::

    [
      name -> "Alice",
      first-appeared-in -> "Alice in Wonderland",
    ]

This is a bag with two key and value pairs. The ``name`` key
references the value ``"Alice"``. And the name ``first-appeared-in``
references the value ``"Alice in Wonderland"``.

An empty record is written as follows, to avoid confusion with
empty lists::

    [->]

We can project values out of records in a similar fashion to
typed data, using the dot operator with the key::

    let Point = [x -> 1, y -> 2];
    Point.x;


Security considerations
'''''''''''''''''''''''

Records are somewhat of a weaker form of Typed Data in Crochet---
we have a structure with some values we can use, but we choose to
neither attach a unique meaning or security policies to it. This
means that records can only be used for public and non-sensitive
information, and are best kept restricted to very local uses---
where we hold on to the record for a short amount of time, and
represent bags of information we'll properly store in typed
data soon.



