What are effects?
=================

In Crochet, Effects are a way of describing the things your program
can do---but without worrying about *how* your program is going to
do these things. This might seem a bit silly at first. Why would
anyone ever need to describe the things a program can do without
describing how the program does them? Isn't having the program
do things precisely why we're writing one?

And sure enough, if it was just a matter of having the program
do things, we could have used commands for that. After all,
looking at commands' signatures tells us what a program does.
And looking at commands' bodies tells us how the program does
those things.

So we need some work on motivating the need for all this "effects"
business. But keep in mind that the *goal* of effects is to make
writing programs in Crochet both safe and flexible.


Intentions, context, and handlers
---------------------------------

Let's imagine you're writing a game that allows players to save
the current state of the game, and later on restore it, so players can
continue playing from their last checkpoint rather than the very
beginning.

To do this, you decide to store the state of the game as a file
in the player's computer. You implement this in your game and things
work just fine. Sometime later, you decide to have your game also
work in a web browser, so people can play it without having to
download anything. "Oh no!", you realise, "you can't save files in
a web browser!"

Unfortunately, your previous decision of using the player's file
system means that you need to rethink your strategy. This requires
significant effort rewriting, but also significant effort to *design*
something that can be used in both contexts.

And what if you wanted to verify that your saving and restoring
functions work correctly? How should you approach that? What about
using them interactively in the IDE? Or debugging it? Suddenly, not
even carefully designing your types and commands to make things 
consistent across all of these contexts would be enough anymore.
You'd need to reach out for more and more complicated concepts.

In order to avoid all of this, Crochet has a principled way of
designing these kind of interactions: Intentions, Contexts, and Handlers.


Intentions
''''''''''

An **Intention** describes, at a conceptual level, what kind of
things your program wants to achieve. In our example we could
say we have two intentions:

- **Saving**: we want to allow players to ask the game to remember
  the current state.

- **Loading**: we want to allow players to ask the game to go back
  to a previously remembered state.

In Crochet, these intentions are captured by effect declarations.
For this case, we could end up with the following::

    effect game-state with
      save(slot is integer);
      load(slot is integer);
    end

We have two cases for this effect: ``save`` and ``load``. The parameters
described here work similarly to type parameters. So, here we allow players
to remember multiple states of the game, by placing each state in a particular
slot.

Once we have this effect declared, we can use the ``perform`` expression
to tell Crochet where we intend for this effects to happen. For example,
we could define ``_ save-at: _`` and ``_ load-from: _`` commands that we
could then use any time we want the game to be saved or loaded::

    command game save-at: Slot =
      perform game-state.save(Slot);

    command game load-from: Slot =
      perform game-state.load(Slot);

By themselves, these commands don't really *do* anything. They just tell
Crochet what our *intentions* are. But we can move on with building our
game by just expressing this first.


Contexts
''''''''

Next we have **Contexts**. A context indicates how we think that
fulfilling these intentions would take place. For example, a context
for our ``game-state`` effect could be the platform that is running
the game---running it in a web browser would require us to think about
game states in a different way from having the same game run directly
on a Windows machine. An android phone would be another different
context.

If our intention was having a way of controlling a game's character,
we could think of contexts as different ways in which this character
could be controlled: players could use gamepads, keyboards, touch
input, voice commands, or even motion capture.

Thinking about more contexts allows us to come up with effect
definitions that are more flexible, though that's not *always* a
goal---remember that the more things you consider, the more work
you might have to do to properly support everything.

For this example, let's consider only "Windows" and "Web Browser"
as our context.


Handlers
''''''''

Finally, we have **Handlers**. A handler specifies *how* effects
should be carried out. For example, let's say that the ``browser``
type provides a way of storing and retrieving data in a web
browser. We could then implement a handler for our effect in
that context as such::

    handle
      Program()
    with
      on game-state.save(Slot) do
        browser at: Slot put: game current-state;
        continue with nothing;
      end

      on game-state.load(Slot) do
        let State = browser at: Slot;
        continue with State;
      end
    end

Here, any part of the program that is executed between the ``handle``
and ``with`` keywords will have the behaviours we specified in the ``on``
handlers for the game-state effect. We similarly need a handler for
when the game runs on Windows, and any other context we plan to support.

But how do we *choose* the right handler based on the context? What is
this ``continue with`` business? In the next chapter we discuss this and
other specifics of handlers.