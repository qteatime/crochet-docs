Signatures and their uses
=========================

So a part of a declaration is made out of (at least) a signature and a
behaviour. But what is a signature, really? Signatures are a combination
of the command's name with the command's requirements. It let us identify
a specific command, or even talk about and search groups of related commands.


Command names
-------------

In the previous section we've seen that command names have an underscore
where requirements and values would go. So, for example, the command
``true and true`` has the name ``_ and _``. But Crochet is actually
quite restricted in which ways names can be formed. One can't just
write something like ``true and true and also true`` and expect Crochet
to understand it as ``_ and _ and also _``.

Crochet has four different "forms" of names:

- **Unary postfix**: these are names like ``_ successor``, ``_ round``, or
  ``_ is-empty``. Note that the name of the command always follows
  the underscore, and when a name is composed of multiple words they
  are written hyphen-separated, rather than space-separated. As the name
  suggests, these commands apply to exactly one value.

- **Unary prefix**: the only name in this category is currently
  ``not _``. Like the postfix variation, only one value is accepted.

- **Binary**: these are names like ``_ + _``, ``_ and _``, or
  ``_ <- _``. These commands have exactly two requirements and
  two values, one on each side of the name. Unlike unary names,
  a binary name cannot be anything you come up with---rather,
  there are a handful of valid names that Crochet knows about,
  and any new name would require a change to the Crochet
  language itself.

- **Keyword**: these are names like ``_ to: _``, ``_ between: _ and: _``,
  ``_ from: _ fold-with: _``. Here the command may have two or more requirements
  and values. It always starts with an underscore. And then is followed by
  any number of ``keyword: _`` suffixes. Like in the unary case, these
  keywords can be anything, and multiple words need to be separated with
  hyphens instead of spaces. Additionally, a colon (``:``) needs to follow
  the keyword immediately---no spaces allowed between the hyphenated words
  and the colon.

- **Self-less keyword**: this is a variation of the **keyword** form where
  the name starts with a keyword instead of a requirement/value. For
  example, ``panic-without-trace: _ tag: _`` and ``panic-without-trace: _``
  are both self-less keyword names. The reason it's called "self-less" is
  that the very first requirement/value in a command is treated in a
  slightly special way in Crochet, and can be referenced through the
  special expression ``self``. A command that does not start with a
  requirement/value would make it confusing to highlight any of them,
  so there's no ``self`` allowed within these commands---they're ``self-less``.
    

Binary command names
--------------------

In Crochet, binary commands cannot have arbitrary names---rather, they must
be one of the pre-defined symbol combinations. One of the reasons for this is that
we want to help people read these consistently, both when they're completely
unfamiliar with the code in question, and when they need to use assistive
technologies to read code. Both of these become much trickier when you
allow arbitrary sequences of symbols to be used for commands.

Crochet does not only prescribe a set of symbolic names, though. It also
prescribes a reading for them, and a meaning for them. This *does* mean
that commands which stray from the meaning prescribed here should probably
choose a different name to avoid confusing users.

The following names are prescribed:

Change operators
''''''''''''''''

``Target <- Value`` (read as: store ``Value`` in ``Target``)
  This is used for any container of data that may change over time. The
  ``Value`` indicates how the ``Target`` will change. ``Target``s may
  hold multiple values, however. And how these values and changes are
  observed is entirely up to the ``Target`` implementation.


Boolean operators
'''''''''''''''''

The semantics for these operators should be close to how one would
reason about boolean algebra.


``A and B`` (read as is)
  This is used for combining two values in a way that produces something
  containing aspects of each side.

``A or B`` (read as is)
  This is used for combining two values in a way that produces something
  containing aspects of one of the sides.

``not A`` (read as is)
  This is used for inverting the meaning of a value.


Equality operators
''''''''''''''''''

The semantics of these operators should strictly follow what is
prescribed by the ``equality`` trait.

``A === B`` (read as: ``A`` equals ``B``)
  This is used strictly for value equality.

``A =/= B`` (read as: ``A`` does not equal ``B``)
  This is used strictly for non-equality of values.


Relational operators
''''''''''''''''''''

These operators are used strictly for ordering of values. The semantics are
prescribed by the ``total-ordering`` and ``partial-ordering`` traits.


``A > B`` (read as: ``A`` is greater than ``B``)
  Used for ordering.

``A >= B`` (read as: ``A`` is greater or equal to ``B``)
  Used for ordering.

``A < B`` (read as: ``A`` is less than ``B``)
  Used for ordering.

``A <= B`` (read as: ``A`` is less or equal to ``B``)
  Used for ordering.

  
Arithmetic operators
''''''''''''''''''''

These operators are used strictly for arithmetic. The semantics are described
by the ``arithmetic`` trait.

``A + B`` (read as: ``A`` plus ``B``)
  Used for arithmetic addition.

``A - B`` (read as: ``A`` minus ``B``)
  Used for arithmetic subtraction.

``A * B`` (read as: ``A`` times ``B``)
  Used for arithmetic multiplication.

``A / B`` (read as: ``A`` divided by ``B``)
  Used for arithmetic division without rounding.

``A % B`` (read as: the remainder of ``A`` divided by ``B``)
  Used for taking the remainder of a division.

``A ** B`` (read as: ``A`` to the power of ``B``)
  Used for exponentiation.


Concatenation operators
'''''''''''''''''''''''

``A ++ B`` (read as: ``A`` followed by ``B``)
  The concatenation operation can be used for anything that can be roughtly
  thought of as the juxtaposition of the two values.


Requirements
------------

So we've discussed names, but what about requirements? Requirements are
what goes into each of those underscores when we're declaring commands in
Crochet.

In their purest form, a requirement looks like this::

    command (Left is integer) + (Right is integer) =
      // behaviour omitted

Both ``Left is integer`` and ``Right is integer`` are requirements. You
can read these as they're written---or in the slightly longer form:
"Left is a value of type integer"---, but what they mean is that whatever
we use at that location must be an instance of the specified type on the
right of ``is``---here our type is ``integer``. And once we've made sure
that the value meets the requirement, we'll be able to refer to that value
by the name that is on the left of ``is``---here it can be ``Left`` or ``Right``.
These names, ``Left`` and ``Right`` are called variables, although in
Crochet, unlike some other languages, they are not allowed to change
what they refer to.

For example, if we had an expression like ``1 + 2``, then ``Left`` would
refer to ``1`` and ``Right`` would refer to ``2``---because both ``1`` and
``2`` are instances of the integer type, and thus fulfill each side's
type requirements.

Besides type requirements, Crochet also supports trait requirements::

    command (Collection is any has countable-container) is-empty =
      // behaviour omitted

In this case you can again read it as it's written, or use the slightly
longer form: "Collection is a value that is an instance of any type, and
has an implementation of the trait countable-container". Here, the
requirement is fulfilled if the value we're using is an instance of the
specified type, and there exists an implementation of the trait
for the any of the types it's an instance of. So in ``[1, 2, 3] is-empty``,
we'd be able to refer to the list ``[1, 2, 3]`` through the name ``Collection``,
because lists implement the trait countable-container.


Multiple trait requirements
'''''''''''''''''''''''''''

A value can have exactly one type, but it can have implementations for
several different traits. So trait requirements allow one to specify
multiple traits, when their combination is necessary.

For example, the collections part of the standard Crochet library relies
heavily on traits for specifying common properties among very different
values---things like sets, lists, and maps can still be handled in a
consistent way if we're only interested in a specific concept that they
all exhibit, but it wouldn't really make sense to turn that into a
*classification* of these types and their relationships.

So, if you look at the standard library, you're going to see several
commands with requirements that look like this::

    command
      (A has set-algebra, countable-container)
      is-subset:
      (B has set-algebra, countable-container)
    =
      (A complement: B) is-empty;

Here we're defining the subset relationship from set theory in a
way that reads: "A is a subset of B if, after removing all B elements
from A, we're left with an empty set---which must mean the B has all
elements that A has, and possibly some more. Note that in order for 
this definition to work we rely on being able to take the complement
of two sets---to be able to take one set, and then remove from it all
elements that are found in another set. This operation is available 
on any type that implements ``set-algebra``. But we also need to be
able to observe if we're left with something that contains any elements
or not. The ``is-operation`` is provided for types that implement
the ``countable-container`` trait.

Trait requirements can specify any number of traits after the ``has``
special word, separating all of them with a comma (``,``).


Convenience forms
'''''''''''''''''

While you can always write requirements in their pure form, it can
be convenient to write it in a shorter form sometimes. For type
requirements we can omit the variables and write just the type
name. With the exception of the special ``self`` value, this leaves
us with no way of referring to the value used at that location,
but it can still be useful when either the type tells us everything
about the value, or when we don't need to use anything from the value
in the particular command.

Throughout the standard Crochet library, the ``self`` requirements
almost always have their variables omitted, and the value is just
referred to by its name within the behaviour. For example::

    command integer successor = self + 1;

This could have just as well been written with an explicit variable,
but here adding a name lengthens the declaration without really
communicating anything new. So the standard library makes the
stylistic choice of omiting redundant information where possible.

We can also omit the type part of the requirement, in which case
the type is treated as ``any``---all types are ultimately instances
of the ``any`` type. Again, being explicit here would be redundant,
as what we want to communicate is that we don't have any specific
requirement on this value---and omitting the type already tells us
exactly that!

We can see this happening in standard library functions like::

    command panic message: Message =
      panic message: Message tag: "panic";

It's a common idiom in commands like the one above, which are
just a convenient way of invoking a different command with some
default pieces filled in. Not having a requirement here means that
the requirements of the real command will be used for all values
we provide here---and it avoids us having to replicate those
requirements and keep them up to date.

For traits, we can also omit the type part---but not the variable part.
Often, for traits, we don't want to stipulate any requirement other 
than an implementation of the trait, so the type requirement is often
just  ``any``---again, that's pretty redundant.

We can see this in standard library functions like::

    command (X has total-ordering) <= (Y has total-ordering) =
      (X < Y) or (X === Y);


A word of caution: ambiguity
''''''''''''''''''''''''''''

Crochet commands can be defined anywhere. By anyone. For any requirements.
But when we put together a program to be loaded by the Crochet VM we need
to make sure that a set of values cannot trigger more than one command.

That is, if we have an expression like ``1 + 2``, then the program is free
to define as many ``_ + _`` commands as it wishes, but there must be exactly
one of these commands which is the "closest match" for that expression.

Crochet will always tell this when you try to load a program---if you have
an ambiguity, that ambiguity will need to be fixed before you can load the
program.

With type requirements, an ambiguity would mean that you have the same
set of type requirements on multiple commands. That is, if you have::

    command true and true = "ok";
    command true and true = "not ok";

Crochet will not be able to load this program because it can't really
know if ``true and true`` should mean ``"ok"`` or ``"not ok"``.

Trait requirements make this problem a bit trickier. Because any type
can implement any trait---and even multiple traits---Crochet gives
all traits the exact same weight. So if we have two different commands
that only depend on traits, they're considered ambiguous by Crochet::

    command (A has countable-container) is-empty = A count === 0;
    command (A has collection-constructor, equality) is-empty = A empty === A;

Here both ``_ is-empty`` commands depend on distinct traits. The second one
even depends on multiple traits. But when you consider that someone could
write the following implementations::

    type set(...);
    implement countable-container for set;
    implement collection-constructor for set;
    implement equality for set;

Then any uses of ``new set(...) is-empty`` could just as well trigger either
of them---there's no relationship between these traits to dictate which one
should be considered "closer" *by the people writing this program*. Sure
Crochet could come up with a disambiguation strategy, but it would be arbitrary
and unlikely to map to most users' expectations. That would mean that using
traits would be even more frustrating than it is now.


Irrelevant variables
''''''''''''''''''''

Names don't always make sense in Crochet, but when using traits it's also
hard to avoid them. For these cases you can use an underscore (``_``) where
the name would go. This underscore tells Crochet that the name isn't really
relevant.

The underscore differs a bit from just picking a random name because we're
allowed to use the underscore in multiple places in the requirement. If we
were to pick a random name, we'd have to pick an unique one for each position
we plan to use it at.

For example, the following would be rejected by Crochet::

    command (X has countable-collection) and: (X has countable-collection) = ...;

That's because Crochet cannot make ``X`` refer to two different values at
the same time---that would be very ambiguous. On the other hand, by using
the underscore we give up on our ability of referring to the values, so
this isn't a problem. Crochet will happilly accept the following::

    command (_ has countable-collection) and: (_ has countable-collection) = ...;

