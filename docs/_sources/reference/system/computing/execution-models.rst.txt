Execution models
================

Computations drive what Crochet can do, but how does Crochet decide
stuff like the order in which these computations are executed? That's
what execution models help answer. Crochet has a few different models
for executing computations, and in this section we discuss all of their
details.


Immediate evaluation
--------------------

The default model Crochet uses to execute programs is called to execute
expressions immediately, often called "eager evaluation". That is,
when a program consists of multiple expressions, Crochet will execute
them one at a time, in the order they're written, only moving to the
next one once the current one finishes executing.

For example, in this piece of code::

    player do-something;
    player do-another-thing;

Crochet would first execute ``player do-something``, and once that
finishes, it would execute ``player do-another-thing``. As if it
was following a step-by-step recipe for cooking something.


Evaluation of sub-expressions
'''''''''''''''''''''''''''''

Whenever sub-expressions are involved, Crochet will execute the
sub-expressions first before it executes the outer expressions.
For example::

    2 + (3 - 4)

Here, Crochet would first execute ``(3 - 4)``, which yields ``-1``,
and then it would execute ``2 + (-1)``, which yields ``1``. When
multiple sub-expressions are involved, Crochet executes things
from left-to-right::

    (1 + 2) + (3 - 4)

Here we first execute ``(1 + 2)``, then ``(3 - 4)``, then ``3 + (-1)``.
Or, in a more visual manner, this would be the steps Crochet takes::

    (1 + 2) + (3 - 4)

    // after executing one step:
    3 + (3 - 4)

    // after executing one step:
    3 + (-1)

    // after executing one step:
    2


When does this matter?
''''''''''''''''''''''

When these expressions are "pure"---that is, when the steps we take
can't be observed---as is usually the case in arithmetic, the order
really doesn't matter. But not all expressions are pure.

Consider the case where a command can display some dialogue to the
player of the game. If we have a piece of code like::

    dialogue show: <<Claris: "May I have some coffee?">>;
    dialogue show: <<Ane: "I will brew it shortly.">>;

Then the player would see this on the screen:

    Claris: "May I have some coffee?"

    Ane: "I will brew it shortly."

The order is very important here, because if we swap these dialogue
lines the entire story ceases to make sense!

We discuss this in more details in the Effects chapter, where we
introduce a tool to better reason and describe these cases.


Partial programs
----------------

By default, Crochet will execute expressions immediately, one
after the other, in the order they're written. This is not always
desirable.

For example, imagine the case where we want to keep only numbers
that are divisible by 2 in a list of numbers. This rule can
be expressed as the Crochet program::

    Item is-divisible-by: 2

However, we cannot execute this program as is because we don't
know what ``Item`` we're talking about. So, for these cases,
we want abstractions. A way of capturing a Crochet program---perhaps
with some additional requirements---and then passing it around
for others to execute.

This is how the ``_ keep-if: _`` command on lists works, in fact.
It takes in a Crochet program and for each item in the list, asks 
that program if the item should be kept in the result. We could write
it like this::

    [1, 2, 3, 4] keep-if: (Item is-disibible-by: 2)

But if we do so, we still run into the same problem as before.
``Item is-disivible-by: 2`` will be executed before we execute
``_ keep-if: _``, and thus we won't know what ``Item`` is again.

The preferred solution for this is to use "partial application".
That is, instead of specifying all of the arguments to a command,
we only specify those that we know, and leave some "holes" for
others to fill in later---thus we capture a Crochet program
that we can pass around for others to execute. We specify holes
by placing an undescore (``_``) character where the argument
would go::

    [1, 2, 3, 4] keep-if: (_ is-divisible-by: 2)

Inside of ``_ keep-if: _`` we'll then fill that hole with some
value. So if the partial program was captured with the name
``Predicate``, this means that ``_ keep-if: _`` would fill the
hole through the syntax ``Predicate(1)``::

    let Predicate = (_ is-divisible-by: 2);
    Predicate(1);

    // Equivalent to:
    1 is-divisible-by: 2;


Applications with multiple holes
''''''''''''''''''''''''''''''''

We can have multiple holes in a command application. This means
that we'll end up with a partial program that has multiple
requirements in order to work. Requirements are filled from
left-to-right.

For example::

    let Between = 5 is-between: _ and: _;
    Between(1, 10);

    // Equivalent to: 
    5 is-between: 1 and: 10;

Holes can be also used when we have a partial program with
multiple requirements, if we're only fulfilling some of them.
For example::

    let Between-for-5 = 5 is-between: _ and: _;
    let Between-for-5-and-10 = Between-for-5(_, 10);
    Between-for-5-and-10(1);

    // Equivalent to:
    5 is-between: 1 and: 10;


Anonymous partial programs
''''''''''''''''''''''''''

Partial programs can be created efficiently by writing a command,
and then specifying only some of its arguments. But sometimes
we may have a slightly larger partial program that we don't
really want to go to the trouble of naming.

In these cases, Crochet allows anonymous partial programs to be
defined within curly braces, and naming all of the holes. For 
example, if we wanted to keep only numbers that are larger than
5, after being multiplied by 2, we could write::

    [1, 2, 3, 4] keep-if: { Number in (Number * 2) > 5 };

Which would be the equivalent of the following::

    command integer double-is-greater-than: Number =
      (self * 2) > Number;

    // And then used as:
    [1, 2, 3, 4] keep-if: (_ double-is-greater-than: 5);
    

Evaluation time in partial programs
'''''''''''''''''''''''''''''''''''

It's important to note that, when a program is partially specified
with holes, all of the non-hole arguments are fully executed before
creating the partial program---so it's their resulting values that
are carried around along with the program.

For example, consider a case where we have a command that takes
two pieces of text, some character name and the line they are
saying, and then formats it appropriately and shows that to the
player::

    command A says: B do
      show: <<[A]: "[B]">>;
    end

If we were to use it like this::

    "Alice" says: "Curiouser and curiouser...";

We would get:

    Alice: "Curiouser and curiouser...";

We could then construct a partial program that captures Alice
saying things, to get the same effect::

    let Alice-Says = "Alice" says: _;

    Alice-Says("Curiouser and curiouser...");

Now, imagine that instead of the Alice's name, we had a
command that shows a short description of Alice before
showing what she's saying::

    singleton alice;

    command alice describe do
      show: "Alice is a young girl in a blue dress.";
      "Alice";
    end

If we had the same program as before, but using this ``alice describe``
command, we'd have end up with the following::

    let Alice-Says = (alice describe) says: _;

    show: "Introduction.";
    Alice-Says("Curiouser and curiouser...");
    Alice-Says("What use is a book without pictures or conversations?");

What we would end up is the following output:

    Alice is a young girl in a blue dress.

    Introduction.

    Alice: "Curiouser and curiouser...";

    Alice: "What use is a book without pictures or conversations?";

So, as we see, ``alice describe`` has been executed right when we
made the partial program. Only the ``"Alice"`` piece of text remained,
which was used when we applied that partial program.

Things work *differently* when we have anonymous partial programs.
No part of an anonymous partial program is executed until the partial
program is applied---and then, the entire program is always executed.
If we had an anonymous partial program instead, as follows::

    let Alice-Says = { What in (alice describe) says: What };

    show: "Introduction.";
    Alice-Says("Curiouser and curiouser...");
    Alice-Says("What use is a book without pictures or conversations?");

We would end up with the following output:

    Introduction.

    Alice is a young girl in a blue dress.

    Alice: "Curiouser and curiouser...";

    Alice: "What use is a book without pictures or conversations?";


Delayed programs
----------------

Sometimes we have a complete program, but we want to delay their
execution until a later point in time. Crochet calls these
"delayed programs".

There are two kinds of delayed programs. The regular delayed
programs are like an anonymous partial program---indeed they use
the same syntax---, but they have no requirements to be fulfilled.

The second kind of delayed programs are "lazy programs". Lazy
programs are a bit special in that they can only be executed
once.


Regular delayed programs
''''''''''''''''''''''''

A regular delayed program has the same syntax as an anonymous
partial program, but without any requirements---because the
program is already complete::

    let Hello = { show: "Hello!" };

Here, ``Hello`` refers to a delayed program. When we execute
this program, nothing will happen. In order to make things
happen, we need to apply the delayed program as before::

    Hello();

Will output:

    Hello!

Delayed programs in this form can be indeed applied multiple
times, and every time we apply them we'll execute the entire
delayed program again, causing any of its effects to also
happen again::

    Hello();
    Hello();

Will output:

    Hello!

    Hello!


Lazy delayed programs
'''''''''''''''''''''

Lazy delayed programs are a bit special. They're described
with the special ``lazy`` syntax::

    let Hello = lazy (show: "Hello!");

Just as before, nothing will have happened at this point.
We'll just have a delayed program referred to by the ``Hello``
name.

In order to apply a lazy delayed program, we use the special
syntax ``force``::

    force Hello;

Will output:

    Hello!

We can force lazy delayed programs multiple times, but they'll
only be executed once::

    force Hello;
    force Hello;

Will output:

    Hello!

The value of lazy delayed programs is rather in capturing
computations that can be expensive. You want to delay doing
that as much as possible, and when you do, you don't want
to do it more than once. For example::

    let Fibonacci-of-55 = lazy (55 fibonacci);

    show: (force Fibonacci-of-55);
    show: (force Fibonacci-of-55);

This will output:

    139 583 862 445

    139 583 862 445
    
But only the first time we force the lazy program will we
actually compute the Fibonacci of 55. When we do so we'll
remember that result, so whenever it's forced again the
remembered result can be returned immediately.