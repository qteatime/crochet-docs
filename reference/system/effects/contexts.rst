Contextual handlers
===================

Having programs depend on intentions---effects---rather than specific
ways these intentions may take form allows us to swap them out depending
on the context without having to change our program's code. This is
important for programs that work in different platforms, with different
capabilities, or just want to change aspects of its execution (as often
needed for testing).

Core to this is the idea of "contexts". But how exactly does one choose
an effect handler based on these contexts?


Reusable handlers
-----------------

First, most of the handlers defined in the standard Crochet libraries
are reusable. They are defined by the package that defines the effect,
and provided through a reusable handler.

For example, in order to use the random number generator package, we
can use the ``scoped-random with-source: _`` handler to run a piece
of Crochet code with that effect::

    let Randomness-source = #random with-seed: 1384172941724;

    handle
      let Random = shared-random instance;
      let A = Random between: 1 and: 10;
      let B = Random between: 1 and: 10;
    with
      use scoped-random with-source: Randomness-source;
    end

The above will choose two integers between 1 and 10 using the source
of randomness that we provided in the ``scoped-random with-source: _``
handler---but only in code that's executed from within the delayed program
we provide in the ``handle`` block.


Execution goals
---------------

Crochet has an idea of "execution goal". These may correlate with
a platform, e.g.: a program may be executed on Windows or on a
Web Browser, and each of those would be a different execution goal.

Goals affect which files are included in the program, and which command is used
to *start* it. For example, in a Web Browser program Crochet will start the
program by executing the ``main-html: _`` command. Whereas, if we're running
the program in Node.js, Crochet would start the program by executing
``main: _``.

A common use of the Novella package for writing interactive fiction that
runs in a Web Browser would define the following entry point command::

    command main-html: Root do
      handle
        novella show: "It was a dark, stormy night...";
      with
        use novella with-root: Root;
      end
    end

Each of these goals has different ideas of which arguments are relevant
for the command. Currently these execution goals are defined in Crochet
itself, and are not customisable. But in the future, applications will
be able to define different execution goals and what it means to run
the program with those goals.
