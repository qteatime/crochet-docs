Naming values
=============

Values can be named in Crochet, but there are a handful of ways in
which they can be named, and each of these ways have slightly
different syntax and rules.


Global Names
------------

One of the first instances of naming a value that you'd encounter
in Crochet is the global name. A global name is introduced by the
``define`` declaration, and it looks like this::

    define one = 1;

So there's a name on the left of the equals, and an expression
at the right of the equals. We can then use this name later to
refer to this value::

    one + 2;

    // Equivalent to:
    1 + 2


Syntactical restrictions
''''''''''''''''''''''''

Not everything is allowed in the ``define`` declaration.
The name must start with a lower case letter, and follows the same
naming restrictions that unary commands and type names do. And the
expression part can only use atomic expressions. That is, within a ``define``
declaration, we can only use expressions that are pure, guaranteed to produce
a value and which can be executed quickly.

This means that we can't write the following in a ``define`` declaration::

    define two = 1 + 1;

Why? Doesn't that look like something that will always produce a value,
and is likely to be executed fairly quickly too? If we consider that the
``_ + _`` command here is arithmetic addition for integers, yes. It should.
But only if the ``_ + _`` command refers to that particular command in
the Crochet standard library---and Crochet doesn't have this guarantee!

It might be that the standard library has not been loaded. Or that
something else defined a ``_ + _`` command that does a different thing.
Crochet cannot really rule out these possibilities, so it takes a more
conservative approach and just forbids any more complex expression
in the ``define`` declaration.

If we really must write these, then we need to use either partial or
delayed programs. For example, this is allowed::

    define two = lazy (1 + 1);

Now every time we want to use this value we also need to evaluate this
delayed program::

    force two + 3

    // Equivalent to (if `two` hasn't been forced before):
    (1 + 1) + 3


Why are they restricted?
''''''''''''''''''''''''

Unlike other declarations in Crochet, a ``define`` declaration will
evaluate a Crochet expression at the time the program is being
loaded. Allowing non-atomic expressions to be used would cause
a few troubles, one of them being that the order in which Crochet
loads code would have to be made relevant.

This sounds weird. Why is making the order relevant such a big deal?
Well, it means that it would be more difficult to make Crochet work
for interactive programming---because besides figuring out how to
let people edit a program, and have these edits have immediate effect,
the tool would also need to figure out how to order these edits!
This is harder than it may sound, as the edits may be in very different
regions of different files.

But the second, and more important issue, is that allowing anything
other than atomic expressions would mean that there could be dangerous
code executing by simply loading a program. Or package. This doesn't
even need to be a program that does *evil* things on purpose. A program
that has a ``define`` declaration that takes too long to finish would
cause problems to the responsiveness of all interactive tools in
the Crochet ecosystem. It could very well prevent a program from
being edited at all!

While Crochet could solve this problem by just making all ``define``
declarations implicitly delayed, Crochet chooses to take the explicit
path instead. Users who really need to write more complex expressions
in a ``define`` declaration can do so by explicitly choosing how to
delay that expression.


Where can global names be used?
'''''''''''''''''''''''''''''''

Global names can be accessed anywhere within the package that declares
them, without any additional effort. Using the name in any expression
will make Crochet pick up the value associated with it, and use that
value.

The names can also be used *outside* of the package that declares them.
In this case, the name of the package also needs to be specified in
order to use them.

For example, if package ``some-package`` defines a name ``one``::

    define one = 1;

Then package ``another-package`` can use it as follows::

    some-package/one + 2

    // Equivalent to:

    1 + 2

This is called a "qualified name"---where the name of the package is
combined with the global name using the ``/`` separator.

We can refer to the global name without using a qualified name by
bringing all names from another package within the possible names
of our package. For example, ``another-package`` above could have
used the ``open`` declaration to bring ``some-package`` names into
its set of possibilities::

    open some-package;

    // Then in an expression:
    one + 2

When we use a global name like this, Crochet will try to search for
a definition with that name in the set of possible names in the package.
This set includes all local names, along with all names in the open
packages.


Local names
-----------

A local name in Crochet---also called a "variable" name---starts
with an uppercase letter, and otherwise can be followed by the same
characters one has in unary command names and type names.

Local names can be introduced in a few different ways. The most
explicit one of them is the ``let`` expression::

    let One = 1;

Here the thing on the left of the equal sign is the name, and the
thing on the right of the equal sign is an expression to evaluate.
The resulting value of evaluating this expression is then associated
with the name.

Local names can also be introduced in a partial program. For example,
in this piece of code we have a partial program that defines two 
local names, ``One`` and ``Two``, and these names are associated 
with the first and second arguments to that partial program::

    { One, Two in One + Two }

Or in a command declaration. Here we similarly introduce two
local names, ``One`` and ``Two``::

    command One plus: Two = One + Two;

Some other special forms, like the ``for .. in .. do``  expression,
also define local names. Here we would associate the local name ``Item``
with each element of the list::

    for Item in [1, 2, 3] do
      show: Item;
    end


When are local names valid?
'''''''''''''''''''''''''''

Local names are valid only in the "region" that declares them. This
is often referred to as the "scope" of the name. In Crochet, these
regions differ, but they're generally delimited by the block in
which the name is introduced.

For example, consider the case of a name introduced by a command.
This is the largest block Crochet has. A name introduced in this
way will be valid anywhere inside of that command---but not outside
of it::

    command One plus: Two do  // -
      One + Two;              // | `One` and `Two` are only valid here
    end                       // -

    define one-plus-two =  // -
      One + Two;           // | `One` and `Two` are not available here,
                           // -  this is a different region.

The region is generally delimited by ``do .. end`` keywords in
most of Crochet's syntax. But some syntax delimits regions with
brackets instead. For example, the anonymous program syntaxes
use curly braces to delimit regions::

    let One = 1;             // - `One` and `Two` are available here
    let Two = {              // |    - 
      let Added = One + 1;   // |    | `Added` is only available here
      Added;                 // |    |
    };                       // |    -
    One + Two;               // _


Reusing names in nested regions
'''''''''''''''''''''''''''''''

A region that nests within another region may use names that are
also used in the outer region. This is generally called "shadowing".
The nested region's name have their own meaning and associations,
and so do the outer region's names. They don't interfere with
each other.

A more concrete way to see this is to think of each region as
persons who knows a set of names and what those names stand for.
You can ask any of these people what a name means, and if they
know the name, they will answer you. If they don't know the
name, they'll ask the person near them---and if there's none,
they will tell you they don't know what the name means.

For example::

    let One = 1;                  // A
    let Two = 2;                  // |
    do                            // |    B
      let One = "one";            // |    |
      show: "[One] [Two]";        // |    |
    end                           // |    |
    show: "[One] [Two]";          // |

Here the ``show: "[One] [Two]"`` expression in the B region would show
``one 2``, as it has its own meaning of the name ``One``, but it needs
to ask the A region about what ``Two`` means.

But the ``show: "[One] [Two]"`` expression in the A region would show
``1 2``, since it has its own meaning of both of those names.


When are names usable?
''''''''''''''''''''''

A local name in Crochet is *valid* from the start to the end of the region
it is declared---that covers parts of the code that appear even before the
name is introduced.

But names are only *usable* after the expression that introduces them is
executed. For example, consider::

    let Two = One + 1;
    let One = 1;

Here ``One`` is valid inside of the expression that introduces the name ``Two``,
but if we were to execute this program Crochet would be confused---at that
point, there's no value associated with ``One`` yet, so execution cannot
proceed.

We can, however, use delayed (and anonymous) programs to work around this.
Because delayed programs aren't *executed* right away, they can use names
that will be introduced later. So long as we actually execute those
programs once all names are introduced, we're good. For example::

    let Two = lazy (One + 1);
    let One = 1;
    force Two;
    
    // Equivalent to:
    1 + 1

