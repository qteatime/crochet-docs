Executing commands
==================

We've seen that the same name might refer to several different commands,
and also briefly touched on how we can refer to a specific command. But
when we're *using* commands, how exactly does Crochet decide which one
to pick and execute? In this section we'll dive deep into the answer to
that question.


Selection and application
-------------------------

When we use a command in Crochet, we only refer to it by its name.
For example, in ``1 + 2`` we're only telling the system "hey, I want
to use the command ``_ + _`` with these two values". But we have no
way of specifying *which* of the ``_ + _`` commands we're talking about.

Many programming languages don't have this problem, because a name
refers to exactly one entity---one function, one procedure, etc. Even
in Crochet, we don't have this problem with types because a name
uniquely identifies a single type. If we say ``1 is integer`` in
Crochet, there's only one type that can go by the name ``integer``,
so the system immediately knows what we're talking about.

So how does Crochet figure out which command we *mean*? Well, it doesn't.
It does not have enough information to be able to figure out what you
wanted to happen. Instead, it does its best to approximate the most likely
meaning from the information available. And then execute the command.

This two-step process consists of **selection**---trying to figure out
which command best approximates your intention, given just a name and
some values. And **application**---the act of actually executing the
command. The combination of these two processes is called **dispatch**.


The selection algorithm
-----------------------

To make sure the approximation Crochet uses is more likely to match
your expectations, Crochet uses a well-defined algorithm for determining
which command to pick. This shared understanding of how selection works
does not mean that Crochet can't do confusing things---rather, it means
that you'll be able to understand why something confusing happened, and then
help Crochet pick the command that more accurately captures what you meant.

Crochet's selection algorithm first picks some candidate commands, by
looking at which commands have their requirements fulfilled by the values
being used. Then it uses the idea of "closeness" to rank these commands.
It then picks up the single top-ranked command to execute.

But what's "closeness"? Every value in Crochet is associated with a type.
And types, which commands use in their requirements, are organised in a
hierarchy. The closest commands are, then, the ones with the more specific
requirements.

Let's see this in a less abstract way. Let's say we're describing plants
in Crochet---the way we *talk* about plants often suggests some hierarchy,
even if we don't think about it that way. In Crochet, we could capture
this plant-hierarchy (or taxonomy) in the following way::

    type plant;
    type flower is plant;
    type rose is flower;
    type white-rose is rose;
    type red-rose is rose;

So, from this declaration we know that a value such as ``new red-rose`` is
a red-rose. But it's also, less specifically, a rose, a flower, and a plant.
And, of course, if we talk about *any* thing, sure we would be including red
roses!

Notice how we have some concept of which of these terms more closely (or more
specifically) describes the ``new red-rose`` value, and which ones less closely
do. Sure we can point at a red rose and say "this is a plant". But that's not
the most specific way we can refer to it, and a plant could be one of several
things. If we say: "plants may or may not have thorns" that's not exactly
*useful* when we're only thinking of red roses. "red roses have thorns" is
a more useful statement. It's a *closer* statement, in Crochet's sense.

So if we had commands that had requirements in this hierarchy, they could
look like this::

    command any has-thorns = "that's a possibility";
    command plant has-thorns = "maybe";
    command flower has-thorns = "maybe";
    command rose has-thorns = "yes";
    command white-rose has-thorns = "definitely";
    command red-rose has-thorns = "you bet";

And if we were to use this ``_ has-thorns`` command with our red rose,
that is, if we had ``(new red-rose) has-thorns`` somewhere in our code,
then Crochet's selection algorithm would first filter these commands.
In this case, we filter out the ``white-rose has-thorns`` command---because
a red rose can never be a white rose, given the hierarchy we've described.

Everything else is still a candidate for being executed, however, so
Crochet proceeds to rank these commands in the following way::

    1.   red-rose has-thorns
    2.   rose has-thorns
    3.   flower has-thorns
    4.   plant has-thorns
    5.   any has-thorns

We've got one command at the very top---ranked in the 1st position:
``red-rose has-thorns``. This what Crochet considers the closest command
that matches what we likely meant by ``(new red-rose) has-thorns``, so
that's the one it will pick.


Ranking trait requirements
''''''''''''''''''''''''''

In addition to type requirements, commands in Crochet may also have
trait requirements. Unlike types, traits in Crochet are not arranged
into any hierarchy, so the idea of closeness that we've previously
discussed doesn't really apply to traits. Even worse: traits can be
implemented by multiple types and it isn't obvious how to think about
which of these implementations and requirements should be considered
"closer".

A trait requirement has the form of ``Variable is type has trait, ...``,
so we still apply the same ranking for type hierarchies that we've seen
before for the ``is type`` part. For the trait part, however, Crochet
assumes that none of them is closer than any other of them. They all
have the same weight, the same specificity, the same closeness.

However, Crochet does define that a requirement that includes traits
is a tiny bit closer than a requirement that does not include traits,
if both of them share the same type requirement. For example::

    command (X is red-rose) smell = "It smells quite nice!";
    command (X is flower has perfume) smell = "It smells nice";
    command (X is flower) smell = "You can't really tell much";

Here, if we were to rank these commands we'd end up with::

    1.  (X is red-rose) smell
    2.  (X is flower has perfume) smell
    3.  (X is flower) smell

Note how, despite being pretty much the same type requirement, the ``_ smell``
command with a trait requirement ranks slightly higher than the one without.

The number of traits in a trait requirement, or the specific traits that
figure in it do not affect the ranking. Crochet only cares if a requirement
includes traits or not.


Selection with multiple requirements
''''''''''''''''''''''''''''''''''''

We've seen how commands can be ranked when we have just one requirement.
But things get a bit more complicated when we have multiple requirements.
For example, consider what happens if we extend our collection of rose
commands to consider multiple of them at the same time::

    command combine: rose and: flower = "A";
    command combine: flower and: rose = "B";

Intuitivelly, we'd expect these commands to have the same requirements.
They both require one rose and one flower on each side. So, if we were
to use this command like so::

    combine: new red-rose and: new white-rose;

Which one of the commands would be selected? What would we get back
from it? In Crochet, the answer would be ``"A"``. That's because
Crochet considers the left-most requirements (the first one in this case)
to have more weight than the right-most requirements (the second one in this case).

So when making a decision to rank these commands, Crochet first looks at
the first requirement of each command and picks the closest one. Then, if
there are still multiple commands that can be selected, it looks at the
second requirement of each command to pick the closest one again. And it
keeps doing so until it runs out of requirements, or only one top ranked
command remains.

So we'd rank the commands above like this::

    1.  combine: rose and: flower
    2.  combine: flower and: rose


Ambiguities in selection
''''''''''''''''''''''''

Sometimes selections are "too successful". That is, with all the information
that Crochet has, it isn't able to pick just one top ranked command---it is
left with several top ranked ones. In these cases Crochet simply cannot
proceed on its own and needs some manual intervention.

But how do these kinds of ambiguity rise? There are three common cases:

- **Uncoordinated definition of commands**: commands can be defined anywhere,
  by anyone, for any type. So it might be the case that you've defined a
  command for some type with a name, and someone else independently defined
  another command for the same type, with the same name.

  Here, you need to pick which of the commands the application will use.

- **Coding mistakes**: because commands can be defined anywhere, one might
  forget that they had already defined a command for some type and try to
  define it again somewhere else.

  Here, you might want to remove one of the command definitions. Or, if
  they're both supposed to exist, you can rename one of them.

- **The use of traits**: because traits don't have a hierarchy, they're
  particularly prone to ambiguities. In these cases you can try to make
  the requirement more specific or rename the command.


What if no command is selected?
'''''''''''''''''''''''''''''''

Sometimes the selection might not be successful at all---there are no commands
whose requirements are fulfilled by the used values. Again, Crochet can't
really do much here on its own and will need manual intervention.

There are three common cases where this failure happens:

- **Mistyping the command**: it's easy to have a typo in the command name
  and not notice it. Sometimes these typos can mean that you get a command
  that exists, but wasn't the one you wanted.
    
  In either case, the way to address this is to fix the typo.

- **High requirements**: it can be that, when you started writing the
  program, you had some view of the requirements in mind, but as you've
  iterated in your design you started relaxing those requirements---but
  didn't get to update them in all of the places.
    
  In this case you might want to update the requirements in those
  commands.

- **Missing commands**: sometimes you might approach writing a program
  through a more wishful approach---you use commands before you actually
  define them; and you only define commands when you're happy with how
  using them feels like. It's easy to forget to define the command later,
  and get this error when trying to run the program.

  Another case where this can happen is if you're using a package written
  by someone else, and you try to provide values to a command that the
  package author had not considered when designing it.

  In both of these cases the only action you can do is define the missing
  commands.


Applying commands
-----------------

We've selected one top ranked command, so Crochet can proceed to applying
that command---executing its behaviour. Application of commands in Crochet
is largely similar to how it happens in other programming languages: we
allow the names described in the command's signature to refer to the
values we've used in that position, and then we execute the command's
body.

That is, consider the following command::

    type person;
    type alice is person;

    enum food = bread, cake, crepe;

    command (Who is person) likes: (What is food) =
      "[Who] likes [What]!";

If we use this command like so::

    alice likes: cake;

Then, inside of that command's body, the variable ``Who`` will refer to the
value ``alice``, the the variable ``What`` will refer to the value ``cake``.
The names refer to the values that appear in the same position when we use
the method. This means that, as an output, we'll get ``"alice likes cake!"``

More specifically, we call the names in the signature, like ``Who`` and ``What``,
parameters. The values that appear when we use the command, like ``alice`` and
``cake`` here, are called arguments.


The ``self`` name
'''''''''''''''''

In Crochet, there exists one very special name called ``self``. This name
will always refer to the left-most argument in an application, as long as
this argument appears before any portion of the command's name.

That is, in ``_ some-command``, ``_ + _``, and ``_ some: _ keyword: _``,
the argument in the position of the first underscore can also be referred
to by the special name ``self``. But this isn't true for the command
``some: _ keyword: _``, because the first underscore here appears after
a portion of the command's name.

Using self, both of the following commands have equivalent behaviour::

    command alice greet = "[self] says, 'Hello!'";

    command (Who is alice) greet = "[Who] says, 'Hello!'";

You might have stumbled with the concept of ``self`` in other languages
by different names. It's often called "the receiver parameter". Sometimes
it's also called by the more confusing term "the method context". Some
languages use ``me`` or ``this`` for this same concept. Ultimately, in
Crochet, ``self`` is just a convenience that relieves you from naming
the first parameter explicitly.
