Traits
======

Types form hierarchies which allow us to classify data---but we get
only a single hierarchy. Say we're modelling a small game where
the player can use different tools to interact with the world.
We could come up with an hierarchy for these tools::

    abstract tool;

    abstract mining-tool is tool;
    type shovel is mining-tool;
    type pick-axe is mining-tool;

    abstract gardening-tool is tool;
    type shears is gardening-tool;
    type watering-can is gardening-tool;

But here we have a problem. We've said that ``shovel`` is a ``mining-tool``,
but a shovel would certainly be useful in gardening too! It could help us
dig the soil and transplant little buds. The problem with describing the
world in terms of Crochet hierarchies is that we can only have one. We
can't have *different perspectives* on a particular type. They have one
inherent classification and that's it. This is intentional.

To overcome this limitation, Crochet allows you to model things in terms
of what they do as well. So instead of thinking of what kind of tool
each of these are, we can think about *what these tools can be used for*.

Our revised hierarchy looks like such::

    abstract tool;
    type shovel is tool;
    type pick-axe is tool;
    type shears is tool;
    type watering-can is tool;

We then complement this with the idea of **traits**. We can only describe
doing things in Crochet through commands, so a trait is essentially a
list of requirements on which commands must be defined for something to
be classified that way.

For example, if we were to have a ``mining`` trait, it could look like this::

    trait mining with
      command Tool mine: (Block is block);
    end

This means that, in order to be a mining tool, we must be able to use the
command ``Tool mine: block`` with it. We could define those for our game::

    command shovel mine: (Block is sand-block) = ...; // more effective
    command shovel mine: (Block is rock-block) = ...; // less effective

    command pick-axe mine: (Block is sand-block) = ...; // less effective
    command pick-axe mine: (Block is rock-block) = ...; // more effective

And we also have to tell Crochet that the provision of these commands is
*intentional*. We're defining them *because* we want these tools to be
a mining tool. We achieve this by using the ``implement`` declaration::

    implement mining for shovel;
    implement mining for pick-axe;

With this it's also fair game for our shovel to be a gardening tool. But
"gardening" is too broad of a category here. We can use the shovel to
dig up holes so we can move or transplant things, but it doesn't really
make sense to use the shovel to water plants. So we have to break down
this category a bit to the specific *uses* that we expect::

    trait transplanting with
      command Tool dig-hole: (Block is block);
      command Tool dig-out: (Plant is plant);
    end

    trait watering with
      command Tool water: (Plant is plant);
    end

This way we can implement ``transplanting`` for shovels and ``watering``
for the watering can.


Intentionality of implementation
--------------------------------

Crochet requires you to not only define all of the commands a trait
requires, but also to tell it "yeah, I'm doing this because I want
to implement this trait". Shouldn't that be obvious?

Sadly, no. And that's only partly due to how Crochet's commands work.
First, commands can be defined anywhere, by anyone. And it's quite
possible that someone may already have defined a command ``_ water: _``
that happens to, accidentally, work for our tools. It would be bad
to consider that to be an intention of being a ``watering`` tool,
only for the command to do something unexpected.

But a slightly more subtle issue is with the human expectations of
a trait. When we come up with a trait we'll have a whole set of
expectations in mind for our little world, but not all of those
expectations are---or can be---captured in the trait declaration.

For example, consider the trait ``equality`` in Crochet's standard
library. It's defined as this::

    trait equality with
      command X === Y;
    end

That's it, just define a `_ === _` command and you're golden. What
this declaration does not tell us, however, is that there's an
expectation that the `_ === _` command works commutatively---that is,
if ``A === B``, then it must also be the case that ``B === A``. We
can swap the values around and still get the same results back.

It would be quite awkward if, I was given a decorated box and a plain
box, and I asked Crochet: "Hey, are the contents of the decorated
box the same as the contents of the plain box?", and the system replied,
"Yes, they are!". But then when I ask, "And are the contents of the plain
box the same as the contents of the decorated box?" it replied, "No,
I'm afraid they aren't".

Requiring people to be intentional about traits means that we can
have a bit more of confidence that these expectations which cannot
be captured in Crochet's code will still be *meaningful*.


Trait relationships
-------------------

Traits do not form hierarchies, in the way types do, however they can
relate to other traits. This happens when, in order to something to
exhibit a particular trait, then it must be the case that they also
exhibit another trait. 

For example, the ``total-ordering`` trait in Crochet's standard library
allows us to ask if something is smaller, bigger, or equal to another
thing. It's defined for numbers, so we can ask questions like, "Is
1 less than 2?" (which in Crochet notation would be ``1 < 2``). We could
define this trait like this::

    trait total-ordering with
      command A < B;
      command A === B;
      command A > B;
    end

But the standard library, instead, defines it this way::

    trait total-ordering with
      requires trait equality;

      command A < B;
      command A > B;
    end

The ``requires trait equality`` declaration tells Crochet that, in order
for something to have a total ordering, it must also have some concept
of equality---the equality trait requires the ``_ === _`` command to be
defined.

Again, the reason to make these relationships is that traits will generally
have some implicit assumptions---some expectations that aren't communicated
in the declaration itself. In the case of equality this expectation is that
if I can say ``A === B``, then I must also be able to say ``B === A`` and
get the same answer back. It has to be commutative.

In the case of total ordering, there's an expectation that for any two values,
we either have ``A < B``, ``A === B``, or ``A > B``. But we cannot have ``A < B``
and ``A > B`` be true at the same time---it doesn't make sense for something
to, at the same time, be smaller and bigger than some other thing. This is
what makes the ordering *total*, in fact.

In this case, the type must declare that it implements both ``total-ordering``
and ``equality``---Crochet does not derive that knowledge from the relationship
we've established. And the reason for this is, again, that these command 
definitions and implement declarations can happen anywhere. Making them
happen implicitly sometimes could be confusing.


Implementing multiple traits
----------------------------

Unlike type hierarchies, we can actually implement multiple traits for a
specific type. That's indeed what they're for. We can *see* a type through
different lenses based on what we want to use them for.

For example, the integer type in the standard library implements the
arithmetic trait---we can use arithmetic operators like ``_ + _`` and ``_ - _``
with them; the equality trait---we can use ``_ === _``; the total ordering
trait---we can use ``_ < _`` and ``_ > _``; and a few others.

In the first example of this section, where we talked about modelling
tools for mining and gardening in a game, there were many types of
mining tools---the shovel being one of them---, but many tools could
also be used for multiple things. We could use a shovel as a mining tool
or a gardening tool.


Testing for traits
------------------

We can test types with the ``is`` operator: ``Tool is shovel`` answers
whether some Tool value is of type ``shovel``. We have a similar test for
traits: ``Tool has mining``---which we can read as "Tool has an implementation
of the ``mining`` trait"---is how we test for traits.

Because a type can implement multiple traits, our trait tests can also
have multiple trait requirements. For example, ``Tool has mining, transplanting``
will succeed if the Tool has both an implementation of the ``mining`` trait and
an implementation of the ``transplanting`` trait.

Trait tests are not transitive---they do not follow trait relationships.
What this means is that if we test for a trait that's required by another trait,
then it would not succeed if the type only declares an implementation on the
more encompassing trait.

In a less abstract way, if we consider that the ``total-ordering`` trait
requires us to implement ``equality`` as well, and we go on to write the
following definitions::

    enum battery = full, half-discharged, almost-gone, gone;
    implement total-ordering for battery;

Then a test for the implementation of total ordering, like
``full has total-ordering``, would succeed. But a test for the
implementation of equality, like ``full has equality``, would not.
Even though we may argue that, if something has a total ordering, then
it must also have an equality.

Crochet does not prevent you from running programs that don't fulfill
all of the specified trait requirements.


Traits in a type hierarchy
''''''''''''''''''''''''''

While trait relationships are not followed, things are a bit more complicated
with types. If a type higher in the hierarchy declares that it implements
a certain trait, then all types below it must also implement that trait.

For example, consider modelling a life simulation game. We could come up
with the following types and traits::

    type being;
    type cat is being;
    type ragdoll is cat;

    trait eating with
      command Being eat: Food;
    end

If we say that being implements the eating trait, then the cat and ragdoll
types must all implement the eating trait too, but they do not need to
*declare* again that they implement it.

That is, we can have the following implementations::

    implement eating for being;

    command ragdoll eat: (Food is cat-food) = ...;

And Crochet would still consider that ``ragdoll`` has the ``eating`` trait
when testing for it, despite not having a more specific declaration of
such.