Branching
=========

Sometimes we may want programs to do different things in certain
conditions. For example, if we're writing a murder-mystery game,
characters might act differently depending on whether the player
is acting as an investigator or a friend of the victim. Often,
these are achieved by listing different things that the program
does for each case we want to consider.

In Crochet, this is achieved by testing for conditions, and
then using branches in the code. This section describes these
tools in more details.


Conditions
----------

The ``condition`` syntax allows one to list a sequence of
conditions and their effects. Crochet will then pick the
first condition that holds---the first condition which evaluates to ``true``---
and execute the effects associated with it.

For example, if we have a rock-paper-scissors game, we can
describe the possible outcomes of the game by using conditions::

    enum move = rock, paper, scissors;

    command (Player is move) against: (Other is move) do
      condition
        when (Player is rock) and (Other is scissors) => "Player wins";
        when (Player is paper) and (Other is rock) => "Player wins";
        when (Player is scissors) and (Other is paper) => "Player wins";

        when (Other is rock) and (Player is scissors) => "Other wins";
        when (Other is paper) and (Player is rock) => "Other wins";
        when (Other is scissors) and (Player is paper) => "Other wins";

        when Player === Other => "It's a draw";
      end
    end

So each condition is specified with the ``when`` keyword, using some
logical test. The effect of this condition can be described as a single
expression with the ``=> Expression`` syntax, or a sequence of expressions
with the ``do ... end`` syntax.

We can also end a list of conditions with the ``otherwise`` keyword. This
always matches, so if every other condition has failed, we'll execute this
effect. ``otherwise`` is just a nicer way of writing ``when true``::

    condition
      when Number < 0 => "It's negative";
      when Number > 0 => "It's positive";
      otherwise => "It's zero";
    end

