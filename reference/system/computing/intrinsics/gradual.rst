Gradual representations
=======================

Expressions in Crochet deal with values, but every value in Crochet has
an associated type. These types are organised in a hierarchy, which allows
us to talk about more general characteristics of values by simply moving
up in this hierarchy---just like we can talk about flowers in general and
have that still include specific flowers, like roses or lilies.

The ``any`` type
----------------

At the root of this hierarchy is the type ``any``. Thus, every value in
Crochet also belongs to the ``any`` type. Anything that we talk
about when we talk about ``any`` must---and will---apply to every value
in Crochet.

``any`` itself is an abstract type, so it can't be constructed. The value
that represents the type ``any`` can still be accessed through ``#any``,
but there's rarely any use for this.


The ``unknown`` type
--------------------

The ``unknown`` type is a container for all types of values which has two
primary functions:

- To be able to represent arbitrary values coming from the outside
  world (e.g.: through the foreign interface) in the Crochet space,
  but without really modelling that value in Crochet; and

- To be able to hide the concrete type of a value, so it can be passed
  around between two places in the code without any of the intermediary
  places having any knowledge of what this value is, or how to manipulate
  it---this is a very important feature for type safety and security.

The first use case is covered in details in the Foreign Interfaces chapter.
But what these two use cases mean is that ``unknown`` is pretty much a kind
of black box---you can pass the box around, but you cannot know what is
inside of it.

From the Crochet side, values can be turned into this black box with the
``_ as unknown`` command. So ``1 as unknown`` creates a black box containing
the number ``1``---a fact that is known internally in the Crochet VM, but not
observable by the Crochet analysis tools, or really anyone else.

In order to recover the value from the black box in the Crochet side, we
need to know what lays inside of it. We once again use the ``_ as _`` command
for this: ``unknown as Type`` will allow us to recover the value from the
black box, as long as we know what ``Type`` is. And then we will be able
to manipulate the value only with the the powers that  ``Type`` grants us.

For example, imagine we first box the integer ``1``. Then we unbox it as
the type ``any``---this will not give us back a value of type ``integer``,
but a value of type ``any``! This means that we'll still be unable to use
arithmetic operators with the unboxed value, as ``any`` doesn't really
know what ``_ + _`` means.

Internally, whenever there's a mismatch between the type we request and
the type of the value in the box---but the type we request is still acceptable---,
Crochet will use a concept called Sealed Types to represent the value
with the exact type we requested, hence preventing anyone who does not
know the specific type to gain access to its powers.


A note on overwrapping
''''''''''''''''''''''

What happens if you try to run ``(1 as unknown) as unknown``? That is, to
take something that is already a black box, and then try to turn it into
another black box.

In Crochet, this operation will give you the same black box. That is, you
cannot put a black box inside of a black box. You can't have an unknown
value that contains another unknown value.


The ``sealed`` type
-------------------

.. warning::

   Sealed types are not implemented in the Crochet VM yet.

A sealed type is a box for values that allows Crochet to see them as a
different type from their specific one. That is, if we have ``1``, we
could seal this value with the ``any`` type, and we would get an integer
value ``1`` which, as far as any Crochet code can observe, acts exactly
like the ``any`` type, and nothing more than that.


The ``nothing`` type
--------------------

The ``nothing`` value is a singleton that is used whenever there is no
other more interesting value to be used.

For example, when we define a command like the following::

    command i-dont-do-anything: _ do
      // No, really, I don't do anything
    end

Whenever we use this command (e.g.: ``i-dont-do-anything: 1``) we'll get
a ``nothing`` value back. That's because commands *always* need to provide
some kind of result, but because we didn't really add any result to this
command definition, Crochet provided something for us.

``nothing`` is also commonly used when we may or may not have a value.
For example, it's common to create hierarchies as follows::

    type branch(more-general, name);

And we could then define a hierarchy like the following::

    let Family = new branch(nothing, "Felidae");
    let Subfamily = new branch(Family, "Felinae");
    let Genus = new branch(Subfamily, "Felis");
    let Species = new branch(Genus, "Felis Catus");

In this snippet of the scientific taxonomy of domestic cats, we've chosen
to stop the hierarchy at the Family level. That means that, if we start
from the domestic cat, the more general we can get is the family Felidae.
And we indicate such by saying that there's ``nothing`` above it.
