Glossary
========

.. glossary::
   :sorted:

   Positional argument
       A positional argument is one whose meaning depends on the position
       it has in a sequence, rather than an explicit name. For example,
       in Crochet, the :ref:`new operator <new-operator>` is positional, because in
       ``new some-type(A, B)``, the meaning of ``A`` and ``B`` would
       change if their order was swapped!

       The opposite concept is a :term:`named argument`. For example,
       records are named in Crochet, so both ``[a -> A, b -> B]`` and
       ``[b -> B, a -> A]`` mean the exact same thing.

   Named argument
       A named argument is one whose meaning is explicitly described by
       a name, and therefore the order in which the arguments are specified
       does not matter. In Crochet, records use named arguments, so
       ``[a -> A, b -> B]`` means the same thing as ``[b -> B, a -> A]``.

       The opposite concept is a :term:`positional argument`. For example,
       lambda applications are positional in Crochet, so ``Lambda(A, B)`` and
       ``Lambda(B, A)`` mean very different things!

   Immutable data
       Data that cannot be changed after it's constructed is called *immutable*.
       Most programming languages will feature things like numbers, such as
       ``1`` and ``2``, which cannot be changed after you construct them. That
       is, you can't make ``1`` mean something else. Crochet extends this idea
       to typed data. If you construct a piece of :ref:`typed data <what-are-types>`
       like ``new point2d(1, 2)``, then it will refer to the coordinates
       ``x = 1, y = 2`` for as long as the program continues to run.

   Projection (of fields)
       Data in Crochet is stored in a bag of information called :ref:`typed data <what-are-types>`.
       Retrieving a particular piece of information from this bag is called
       a *projection*---you're "projecting" a certain aspect of the data outside
       of the bag. Projection is handled by the :ref:`dot (.) operator <field-projection>`.