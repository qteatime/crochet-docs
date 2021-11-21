Contracts
=========

.. warning::
  
   Contracts are largely a work in progress. Crochet is currently missing
   ways of reusing contracts and applying contracts to more complex
   concepts.

While example-based testing lets us describe specific scenarios of
our programs and what we expect to happen in them, contracts allow
us to specify things that always have to be true.

Currently Crochet allows contracts to be specified for commands only.


Pre- and post-conditions
------------------------

Crochet's contracts for commands come in the form of pre- and
post-conditions. A pre-condition describes things that need to
be true about the program before the command is executed, whereas
a post-condition describes things that need to be true after the
command is executed.

For example, consider the case where we're building an inventory,
and we have a command to take something out of the inventory. Here,
a pre-condition could be that the item exists in the inventory,
and the post-condition could be that the item does not exist
in the inventory anymore.

If we were to express this in Crochet, it could take this form::

    command inventory remove: Item
    requires
      item-exists :: self.items contains: Item
    ensures
      item-removed :: not (self.items contains: Item)
    do
      // The code for the command goes here
    end

In the ``requires`` section of the command we specify all of the
properties that have to be true before it executes. Here we have
just one: ``item-exists``, which says that whatever we're trying
to remove must exist in the inventory to begin with.

The ``ensures`` section describe the same for post-conditions.
Both pre-conditions and post-conditions may contain several
of these properties, each of them separated by a comma.

For example, the ``integer to: _ by: _`` command gives us a
sequence where we start with a number, and keep adding some
small increment to it until we reach a given limit. The contract
for this command specifies two pre-conditions::

    command (Start is integer) to: (End is integer) by: (Step is integer)
    requires
      progress :: Step > 0,
      ordered :: Start <= End
    do
      // Implementation intentionally omitted
    end

Here, the ``progress`` property ensures that we can get a
sequence at all. If someone provided a step of 0 by mistake,
the command would never be able to finish---adding zero to
any number just gives us that number!

We also care about the sequence being ``ordered``---the ending
number must be greater than the starting number, otherwise we'll
never be able to reach it.