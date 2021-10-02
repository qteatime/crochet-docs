Types and data modelling
========================

What are types?
---------------

A type is primarily a way of classifying data. For example, a number like
``1`` is classified as an `integer`_. A piece of text like ``"hello"``
may be classified as a `text`_. A value like ``true`` can be classified
as `boolean`_.

Crochet uses these classifications both to talk about data in a more
general way---making it a tool for people to communicate with others---,
and also a tool to define what can and can't be done to pieces of
data. That makes types double as a privacy and security feature as
well.

This means that, in Crochet, a "type" is:

- **A way of granting `Dynamic Capabilities`_** ---
  Types are the sole grantors of dynamic capabilities. What a piece of code
  can do depends entirely on which types it has access to, and what it can
  do with those types.

- **A way of doing `Dispatch`_** ---
  Crochet's `Commands`_ are a collection of different functions, and the
  runtime uses types to select which one of these functions should be
  executed for some given arguments. ``A + B`` may do very different
  things depending on what the types of ``A`` and ``B`` are.

- **A way of classifying and securing data** ---
  Crochet's types are also `Runtime Tags`_, and they provide a way to
  classify and secure data at runtime.


.. _type-declaration:

Type declarations and usage
---------------------------

A type declaration provides a name for a particular combination of data.
For example::

    type point2d(x, y);

Here, ``point2d`` is a name that will be associated with a combination
of data that contains ``x`` and ``y`` points. Here, ``x`` and ``y`` are 
also called `fields`_. Association is done through the `new operator`_::

    new point2d(1, 2);

Will associate the name ``point2d`` with the data points ``x = 1`` and
``y = 2``. Important to Crochet's security guarantees is that this
name association is `unforgeable`_. One must know and have power over
the ``point2d`` declaration in order to associate it with data points.

Once a piece of data is associated with a name, specific fields of
this data can be projected with the `dot operator`_::

    let P = new point2d(1, 2);
    assert P.x ==> 1;
    assert P.y ==> 2;

`Field projection`_ is very restricted for security reasons, and typed
data is really mostly operated (and observed) through `commands`_.


.. important::

   What constitutes a valid spelling of a type name in Crochet is
   very restricted. The section on the :ref:`lexical restriction of names <lexical-restriction-names>`
   discusses this in details.


.. _typed-fields:

Fields of typed data
--------------------

Typed data consists of an unique, unforgeable name (the type) and a set of
fields. Each field is a named piece of data, bound at the time it's constructed,
and unchangeable henceafter. That is, unlike many object-oriented languages,
all fields in Crochet are effectively :term:`immutable <immutable data>`.

Although fields describe what some kind of "shape" for the data---that is,
what the typed data is constituted of---, fields don't really determine
how Crochet stores this data in a computer. The :ref:`internal layout <internal-data-layout>`
of a piece of typed data is a bit more complicated, and subject to constant
changes.

.. important::

   What constitutes a valid spelling of a field name in Crochet is
   very restricted. The section on the :ref:`lexical restriction of names <lexical-restriction-names>`
   discusses this in details.


Global fields
'''''''''''''

Because fields may carry very sensitive pieces of data, by default they're
restricted and can only be accessed within the package that declared the
type. In order to make them accessible outside of the package, one needs
to expose them through a `command`_.

Some types have very trivial patterns for accessing their fields, however.
For example, if we have::

    type point2d(x, y);

Then we don't really want to do anything before providing the values stored
in ``x`` and ``y`` to whoever needs them. So we'd essentially be writing::

    type point2d(x, y);
    command point2d x = self.x;
    command point2d y = self.y;

In these cases, we can mark the field as "global" and Crochet will generate
the command definitions above for us. So the following is equivalent, but
takes less effort::

    type point2d(global x, global y);


Data-less types
---------------

Types are often associated with pieces of data to control how we can
observe and operate on them, but they're not *always* associated with
a piece of data. For example, types like ``nothing`` stand on their
own, they don't need to be associated with anything else.

A data-less type declaration looks much like what we've seen previously,
but no fields are specified::

    type some-name;

The `new operator`_ is still what brings these types to the realm of
data---but there's no data to associate with the name. Data-less types
are, instead, used to build unforgeable and unique names. These names
can have many usages. For example, these names can act as a way to
identify related data: if you're building a game, characters may be
data-less types whose actual data is stored elsewhere, like in
`Crochet's database`_. They are also often used to define `modules`_,
or as a `secure capability`_.

However one decides to use them, construction is similar, but again
without providing any field bindings::

    new some-name;


Singleton types
---------------

A special form of a data-less type is one where we don't really want
to construct multiple unique names. Rather, we want to have one name
that is unique and unforgeable. `modules`_ often fall in this category,
but so do a lot of the other cases mentioned previously. For example,
if you're building a game, and you're using a data-less type for a
main character, you don't really want to have *multiple* unique copies
of that character.

Crochet provides a special type declaration for this::

    singleton player;


In this case we don't use the :ref:`new operator <new-operator>` for materialising the
name ``player``---it's already part of the ``singleton`` declaration.
It will construct a global name ``player`` that is unique.

Indeed, the singleton declaration works much like the following
piece of Crochet::

    // Introduces a new data-less type definition, `player`.
    type player;

    // Constructs an unique `player` name, allows it to be accessed through
    // the global `player` variable.
    define player = new player;

    // Forbids any further construction of `player` names.
    seal player;

The `seal`_ operation at the end ensures that the system has exactly
one ``player`` name, by forbiding any future uses of the :ref:`new operator <new-operator>`
for this type. This guarantee is useful when using these names as keys
(e.g.: when using them as keys in the `Crochet database`_), as it
eliminates the potential for confusion when copies of the name
are created accidentally.


Types as possibilities
----------------------

There's one more data modelling aspect that is not covered by the previous
type declarations. Consider the case where we want to talk about
mathematical shapes. Sure we can just define each shape independently::

    type square(side);
    type circle(radius);
    type triangle(adjacent, opposite, hypotenuse);

But these independent definitions obscure that all of them share some
commonality; all of them are shapes. It gives us no language to talk
about shapes, in general, only particular shapes.

To address this, Crochet uses `subtyping`_ relationships. That is, types
are placed into a `hierarchy`_, and types that are higher in the
hierarchy can be used to talk about some commonalities of the
types below them.

In this case, we could introduce a ``shape`` type that sits atop of
these specific shapes::

    type shape;
    type square(side) is shape;
    type circle(radius) is shape;
    type triangle(adjacent, opposite, hypotenuse) is shape;

Note the ``is shape`` attached at the end of the previous type declarations.
It denotes that each of these individual shapes can also be understood as
a ``shape``. A `command`_ that accepts ``shape``s will accept any of the
specific ones, as well as ``shape`` itself.


Caveats of a static hierarchy
'''''''''''''''''''''''''''''

It's important to note that Crochet admits only one static hierarchy. This
is discussed at length in the `subtyping and hierarchy`_ section. But it
means that this feature is a poor fit for *contextual* hierarchies. For
example, still in the theme of mathematical shapes, one may think that
a ``square`` would be just a special case of a ``rectangle``, and they
may proceed to define the following hierarchy::

    type rectangle(width, height) is shape;
    type square(side) is rectangle;

You might think that this makes sense, but we run into things like the
following::

    let A = new rectangle(10, 10);
    let B = new square(10);

Now, both ``A`` and ``B`` are mathematically equivalent shapes---they're
both squares with sides of length 10. But Crochet's type system does not
know that a square means "all sides have equal length", it only knows that
rectangles have a ``width`` and ``height`` component, and squares, which
are a kind of rectangle, only have a ``side`` component. Therefore the
type system does not consider ``A`` to be a square---even though we,
humans, do.

So, as a rule of thumb, it's better to make subtypes only if they
unconditionally fulfill all of the properties of its parent type. Such
principle is often described as the `Liskov substution principle`_.


Caveats of an open hierarchy
''''''''''''''''''''''''''''

It's important to note as well that hierarchies in Crochet are **open**.
This---and its implications---is discussed at length in the
`subtyping and hierarchy`_ section. But it means that new types may
be added to the hierarchy at any point in time, by anyone.

For example, consider the case where one is modelling an RPG system
where characters may be affected by different conditions. This will
often be defined as an hierarchy, so we can talk about *conditions*
in general, as well as specific conditions::

    type condition;
    type poisoned is condition;
    type sleeping is condition;
    type silenced is condition;

As it stands, the author of the ``condition`` type has thought of
three different conditions: ``poisoned``, ``sleeping``, and ``silenced``.
It's quite likely that the code dealing with conditions may end up 
baking assumptions about its specific conditions. However, there is
nothing in Crochet that prevents some other piece of code from
attaching more conditions to this hierarchy::

    type petrified is condition;

If such a declaration appears at some later point, somewhere in the
program, then ``petrified`` will be considered as much as a member
of the ``condition`` hierarchy as any other. These declarations may,
indeed, happen when the program is executing---through the
`Crochet interactive playground`_.

In order to add new types to the hierarchy, however, an author would
need to have access to the ``condition`` type. So limiting the visibility
of this type would allow more control over the hierarchy. But the
open and extensible behaviour is often more desirable if you're
sharing your code with someone else.


Caveats of field projection
'''''''''''''''''''''''''''

Often programming languages that feature type hierarchies also have
subtypes inherit the fields from the parent type. That is, given
something like::

    type rectangle(width, height);
    type square(side) is rectangle;

Then, in common object-oriented languages, the ``square`` type would really
define three fields: ``width``, ``height``, and ``side``. Where the first two
would be inherited from ``rectangle``.

Crochet does not work that way. In Crochet, there is no field inheritance.
The layout of a data structure is precisely what is specified in its
declaration. Commands, however, are inherited, and thus it is important
for inherited commands to not use field projection directly.

This is discussed at length in the `subtyping and hierarchy`_ section.


Abstract types
--------------

Types that exist only to denote an hierarchy are often not really *useful*
to construct. For example, in our previous examples with the ``shape`` and
``condition`` types, there aren't really use cases for constructing them.
Crochet makes it possible to make this explicit through the ``abstract``
declaration::

    abstract shape;
    type square(side) is shape;
    type circle(radius) is shape;
    type triangle(adjacent, opposite, hypotenuse) is shape;

Here the only thing that has changed is the declaration of the ``shape``
type, replacing the ``type`` keyword with the ``abstract`` one. The
semantics of the ``shape`` type (and any of its subtypes) remain largely
unchanged, but this means that the :ref:`new operator <new-operator>` will not work on
``shape`` itself::

    new shape;
    // *** Error: non-constructable: `shape` is an abstract type;
    //                                it cannot be constructed.


Enumeration types
-----------------

Sometimes you want an hierarchy of names, just like the example of
modelling a ``condition`` hierarchy for an RPG earlier in this
page. The specific subtypes don't really need to hold any data,
but you'd like to differentiate each case.

While it's possible to just provide all cases one by one, using
the ``is <parent type>`` notation, Crochet provides a more
convenient way of declaring these hierarchies; called an
`enumeration`_.

Enumerations in Crochet can be declared as follows::

    enum condition = poisoned, sleeping, silenced;

The effect is similar to the following way of declaring the same::

    abstract condition;
    singleton poisoned is condition;
    singleton sleeping is condition;
    singleton silenced is condition;
    close condition;

However, enumerations are `closed hierarchies`_, meaning that it is not
possible to add new names to the hierarchy somewhere else in the code.
All possibilities must be provided at the exact place where the enumeration
is declared.

Enumerations make use of this additional restriction to provide some
out-of-the-box functionality. For example, enumerations are *ordered*,
which makes them useful for modelling a set of progressive states---or
steps::

    enum health = healthy, scratched, bleeding, dead;

In a game that features combat and tracks the health of characters without
using numbers, the above would offer a possibility of using pre-built
commands, such as ``healthy successor`` to move a character who just
took some damage to the ``scratched`` state.

See the `Enumerations`_ page for a lengthy discussion on these built-in
conveniences.


Static types
------------

We've seen how types are unique, unforgeable names that can be associated
with a piece of data (or with nothing, in the case of data-less types).
When one constructs a type through the :ref:`new operator <new-operator>`, we get an
unique piece of data. But until we do so, types don't really play in
the same field data does---types are entirely separated entities,
operated on only through ``type`` declarations.

This creates some awkward problems, however. For example, consider 
integral numbers, such as ``1`` and ``2022``. In Crochet, these are
all associated with the `integer`_ type. And when we define `commands`_
on this integer type, we only accept actual integral numbers in them.
For example, ``1 + 2`` is integral addition, but ``integer + integer``
is not even valid Crochet code, because types cannot appear there.
What, then, should a command about integers look like when you don't
have an actual number to provide, because the command is responsible
for producing them?

To be more concrete, consider the case of taking a textual
representation of integral numbers, such as ``"one"``, and producing
the equivalent integer---which in this case would be ``1``. A language
may be tempted to define a command on pieces of text, such as::

    command text to-integer = // implementation goes here

But command names in Crochet are neither unique nor unforgeable. We
may have two different people introducing an ``integer`` type and
that will result in two distinct types. Commands don't allow this.
Naming two commands ``to-integer`` just means that you need to
pick which one will be used; you can't have both. And this runs
against all of the `security guarantees`_ that Crochet relies on.

So, instead, Crochet has a special notation for using types without
constructing them. When directly turning types into data, the resulting
data is going to be associated with a *static type*---a special version
of the type, with the same name, but which isn't part of any `hierarchy`_.

Types are turned into static data by prefixing their name with ``#``. It
means the special static type when in a type context, and the unique 
static data when in a data context. So, if we were to write a more secure
version of the previous command, we could do as follows::

    command text to: #integer = // implementation goes here

And this would be used like so: ``"one" to: #integer``, resulting in ``1``.

Indeed, these conversion cases are common enough that Crochet has the
command `_ as _`_ in the standard library.

.. attention::

   Static types are very limited. They cannot be used in ``is <parent>``
   relationships, and they do not have any further static types. That is,
   something like ``##integer`` (the static type of the static type of integer)
   is not a valid piece of code in Crochet.