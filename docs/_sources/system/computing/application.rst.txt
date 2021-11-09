Applying programs and commands
==============================

In the Commands chapter we've touched briefly how commands are
executed, but there's a few more general things to cover when
it comes to how delayed/partial programs and commands are
executed in general.


Application in a nutshell
-------------------------

We execute programs and commands by applying them to some
values---or to no values, in the case of nullary functions
and thunks. The form of this "application" varies depending on which
kind of thing we're trying to execute. 

Commands
''''''''

For commands, the application follows the same syntax we've used to declare
the command. That is, if we declare a command like this::

    command A + B = // body omitted...

Then we could execute it with::

    1 + 2

Likewise, if we declare a command like::

    command A then: B and-finally: C = // body omitted...

We'd execute it with::

    1 then: 2 and-finally: 3

So the expressions that compute a value will always
go in the same place requirements appear in the command
declaration.

Functions
'''''''''

This is not the case for partial programs. If we have
a partial program like the following::

    let Add-one = _ + 1;

Then we *always* apply it by suffixing the program
with a parenthesised list of values---which should
match the number of requirements we have::

    Add-one(2);

The same is true for regular delayed programs, and
partial programs created with curly brackets::

    let Hello = { show: "Hello" };
    let Add-two = { A in A + 2 };

    Hello();
    Add-two(3);

Thunks
''''''

Thunks are yet another case. When we have a lazy
delayed program (or thunk) like the following::

    let Three = lazy (1 + 2);

Then our only way of applying this is by using the
``force`` special syntax::

    force Three;


Precedence
----------

When we have more complex applications, how exactly do we tell Crochet
which one goes first? Crochet has an internal idea of precedence
in its notation that decides this. This is similar to
the convention you might have seen in school for arithmetic expressions.
Crochet's convention has less rules though.

In Crochet, we first execute function applications, then unary command
applications, then binary command applications, and finally keyword
command applications.

That is, if we have the following expression::

    1 + 2 is-disivible-by: Three() * 2 successor

Then Crochet will see this, more explicitly, as the following parenthesised
expression::

    (1 + 2) is-divisible-by: ((Three()) * (2 successor))

Meaning that we'll first execute ``1 + 2``. Then we'll execute ``Three()``,
then we'll execute ``2 successor``. Then ``_ * _`` with the result of those
two. And finally ``_ is-divisible-by: _``.


A note on arithmetic convention
'''''''''''''''''''''''''''''''

You might have learned in algebra classes that, in arithmetic expressions,
there's a common convention of performing multiplication before addition, 
and so on. There's no such convention in Crochet. If you write the
following arithmetic expression::

    1 + 2 * 3

Crochet will complain, loudly, that your expression is ambiguous, and will
refuse to execute this program. To fix it you need to explicitly
parenthesise the expressions and decide which one should be executed first.
The following are both valid, but compute different values::

    (1 + 2) * 3;    // this results in 9

    1 + (2 * 3);    // this results in 7

There is, however, an exception to this. It is possible to combine associative
binary commands without parenthesis---that is, if Crochet has a guarantee that
the different groupings of the operations will not affect the result,
then it's not a problem to combine them without parenthesis. This is only true as far
as the unparenthesised operator is the same. In Crochet, the ``_ ++ _``, ``_ + _``,
``_ * _``, ``_ and _``, and ``_ or _`` operators are associative. Meaning
that the following expressions are valid::

    1 + 2 + 3 + 4;    // always results in 10

    1 * 2 * 3 * 4;    // always results in 24

    [1] ++ [2] ++ [3] ++ [4]  // always results in [1, 2, 3, 4]

    true and true and false;  // always results in false

    true or true or false;    // always results in true

Everything else needs to be parenthesised.


Associativity
-------------

When we're dealing with unparenthesised, complex expressions, they
may be grouped differently depending on how they associate. Things
can be left-associative (parenthesis favour things to the left) or
right-associative (parenthesis favour things to the right).
Expressions in Crochet are *always* left-associative.

That is, if we have a sequence of arithmetic addition, like the
following::

    1 + 2 + 3 + 4

Then Crochet will see this expression as follows::

    (((1 + 2) + 3) + 4)

Note how the parenthesis start on the left and gradually extend
to embrace expressions more to the right. This plays into the
guarantee that Crochet also executes code more to the left first.

Associativity doesn't play as much of a role in Crochet as it
might in other programming languages, however, because we only
allow unparenthesised expressions that are commutative. That is,
the result of the entire unparenthesised must be the same regardless
of which order Crochet decides to execute it in any case. However,
thinking about the particular order Crochet chooses might be important
when thinking about performance.


Pipes
-----

Because the precedence rules in Crochet say that keyword commands
always have the same precedence, it's not possible to combine them
without using parenthesis, or storing intermediary results in
variables. This makes things a bit inconvenient when these commands
are fairly common.

For example, consider the case where you may be trying to shape
a collection of moves by their effectiveness. You could write
code that looks like the following::

    // Get the list of moves the player can use now
    let Moves = player available-moves;

    // Compute the effectiveness of each possible move
    let Moves-with-effectiveness = Moves map: (_ compute-effectiveness);

    // Keep the more effective moves first
    let Sorted-moves-with-effectiveness =
      Moves-with-effectiveness sort-descending-by: (_ effectiveness);

    // We only care about the name of the move
    let Move-names = Sorted-moves-with-effectiveness map: (_ name);

This works, but the names we're using don't really help us much
with reading the program---in fact, because they take so much
space stating things that are already there, it ends up making
programs a bit more cumbersome to read. And while we could get
rid of names by using parenthesis, doing so makes it even worse::

    ((((player available-moves)
          map: (_ compute-effectiveness))
            sort-descending-by: (_ effectiveness))
              map: (_ name));

Even trying to use the layout of the code to hint at how each of
these expressions are related is fraught. The parenthesis are not
just distracting---they take too much effort to maintain, too.

For these cases, Crochet allows the use of "pipes" instead. A pipe
allows one to apply a command to the result of a previous command.
With this we can create a sort of "pipeline", which tells Crochet:
"First do this, then do this other thing to that result, and then
this other thing, and then...".

Using the the pipe command application syntax (``|``) our code would read
like this instead::

    player available-moves
      | map: (_ compute-effectiveness)
      | sort-descending-by: (_ effectiveness)
      | map: (_ name);


Functional pipes
''''''''''''''''

The pipe command application syntax is restricted to a single command
at the right, and the result is always taken to be the first argument
for that command. With the way Crochet is designed, this is often
what you want, and it reduces the amount of plumbing you need to
care about.

Sometimes, however, you need a bit more of flexibility. Function
application pipes are an alternative for building pipelines where
we have more arbitrary expressions, or the target for the result
flowing through the pipeline is not always the first argument.
Functional pipelines use the ``|>`` syntax, and expect a partial
program with one parameter on its right.

Using partial application and functional pipelines we would get
the following::

    player available-moves
      |> _ map: (_ compute-effectiveness)
      |> _ sort-descending-by: (_ effectiveness)
      |> _ map: (_ name);

