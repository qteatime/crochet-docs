Hierarchies of types
====================

Types in Crochet are organised into a hierarchy. This hierarchy
is described by the way types are defined.

For example::

    type being;
    
    type person is being;
    type alissa is person;
    
    type cat is being;
    type caramel is cat;


These types describes a taxonomy---a classification of different
kinds of things into a hierarchy. From this classification we
know that caramel is a cat. But also, transitively, caramel is
a being---because all cats are also beings. Likewise, alissa
is a person and also a being.

All of them are also, implicitly, "any"---because that's the
root of Crochet's hierarchy. When we talk about "any"thing,
then it makes sense that we could possibly be talking about
any of these types.

We can visualise this hierarchy like so::

    + any
    |
    `--+ being
       |
       `--+ person
       |  |
       |  `--o alissa
       |
       `--+ cat
          |
          `--o caramel


Modelling possibilities
-----------------------

Hierarchies are used for Dispatch, but they're also a tool for
reasoning about programs and designing programs in Crochet.
One such design approach is to use types to capture the
possibilities in the little world we're creating in our
programs.

For example, suppose we're writing a program that simulates
flipping a coin. We toss the coin up, and when it falls it's
going to give us some result. We can capture this result as
a possibility::

    type coin-result;

Now, there are really only two results we can get: when the
coin falls, it'll land with one or the other side up. These
sides are generally called ``head`` and ``tail``, so we
can model these as discrete possibilities of a coin result::

    type head is coin-result;
    type tail is coin-result;

Of course, there's still a remote possibility that, if we
were to more accurately capture physics and complex
environments, the coin never lands on either side! In that
case, there's no real result and we should flip it again.
But it's still interesting to capture this as a possibility::

    type undecided is coin-result;

By capturing this as a hierarchy not only do we get to see
what are the things that can happen when we flip a coin, and
talk about the specific results that we may get. It also lets
us talk about results *in general*.


Caveats of a static hierarchy
'''''''''''''''''''''''''''''

It's important to note that Crochet admits only one static
hierarchy. This means that the feature is a poor fit for
*contextual* hierarchies.

For example, if we think about mathematical shapes, then
a ``square`` would be just a special case of a ``rectangle``,
and we may proceed to define the following hierarchy::

    type rectangle(width, height) is shape;
    type square(side) is rectangle;

At first, this might make sense, but we run into cases like the
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
unconditionally fulfill all of the properties of its parent type. 
This is often described as the Liskov substution principle.


Caveats of an open hierarchy
''''''''''''''''''''''''''''

It's important to note as well that hierarchies in Crochet are **open**.
This means that new types may be added to the hierarchy at any point
in time, by anyone.

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
Crochet interactive playground.

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


Testing classifications
-----------------------

Once we have a hierarchy of types, it's useful to ask the system questions
like "is X a cat?", where ``X`` can be any Crochet value. Crochet then
allows the program to behave differently depending on the answer to that
question.

For example, if we were to model a rock-paper-scissors classification::

    abstract move;
    singleton rock is move;
    singleton paper is move;
    singleton scissors is move;

Then we could determine the winning move of this game by testing for
this classification::

    condition
      when (A is rock) and (B is scissors) => "A wins";
      when (A is paper) and (B is rock) => "A wins";
      when (A is scissors) and (B is paper) => "A wins";

      when (B is rock) and (A is scissors) => "B wins";
      when (B is paper) and (A is rock) => "B wins";
      when (B is scissors) and (A is paper) => "B wins";

      otherwise => "It's a draw";
    end

The ``Value is type`` expression allows us to ask Crochet questions
about the classification of the value in the type hierarchy we've
defined. This will be true whenever the value's type is the same
as the one we're asking about, of course. But it'll be also true if
the type we're testing is any of the parents of the value's type.
The value ``rock`` is of type ``rock``, but also of type ``move``,
and also of type ``any``.

The recommended way of testing for classifications in Crochet, however
is to use commands. We can specify type requirements in commands, and
new commands can be defined at any point later, if these need to be
adapted or extended to a different context. With commands our example
before would look like this::

    command move beats: move = false;
    command rock beats: scissors = true;
    command paper beats: rock = true;
    command scissors beats: paper = true;

    command (A is move) play-against: (B is move) =
      condition
        when A beats: B => "A wins";
        when B beats: A => "B wins";
        otherwise => "It's a draw";
      end;

In ``move beats: move``, we're defining a base line for all moves.
If we don't know what specific move has been used, then we can't
truly say which one wins in the game. But we follow that by defining
different commands for each specific type. ``rock beats: scissors``
captures one of these specific commands, where we override our base
line with a more informed behaviour for this game.

Commands and dispatch are discussed in details in the commands chapter.
