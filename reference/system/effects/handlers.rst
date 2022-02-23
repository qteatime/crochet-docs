Effect handlers
===============

An effect handler tells Crochet what should happen when an effect
is *performed*. These handlers are specified in special
``handle ... with ... end`` blocks, where we wrap some piece of
code and specify how we want certain effects to behave.

For example::


    handle
      let A = perform counter.next();
      let B = perform counter.next();
      A + B
    with
      on counter.next() do
        continue with 1;
      end
    end

Here, we perform the effect ``counter.next()`` twice. Each of these
times we'll run the piece of code in the corresponding ``on`` handler.
Our particular handler here only has one expression which says
``continue with 1``. This means that, as a result of "performing"
this effect, we'll get the value ``1``. So both ``A`` and ``B`` will
refer to 1.


Handling an effect
------------------

What happens when we ask Crochet to perform an effect? Well, it will
try to find the closest matching handler and execute it. For example::


    handle
      let Result = perform greet.hello();
      Result + 1;
    with
      on greet.hello() do
        show: "Hello!";
        continue with 1;
      end
    end

Will look at its enclosing ``handle`` block, and then notice that we
do have a handler for the ``greet.hello`` effect. So we execute it,
showing ``Hello!`` to the user, and continue from where we stopped
with ``1``. This value is associated with the variable ``Result``,
and we proceed to return ``Result + 1``---that is, ``2``.

In a more visual way, we can think of handles and performs working
as follows. First we see the handle block, so we keep track of what
handlers it provides to us. In this example we have a handler for
``greet.hello``, so our handlers look like this::

    // Current handlers:
    on greet.hello() do
      show: "Hello!";
      continue with 1;
    end

We then move on to the piece of code inside the handle block::

    // Current handlers:
    on greet.hello() do
      show: "Hello!";
      continue with 1;
    end

    // Now running:
    let Result = perform greet.hello();
    Result + 1;

So the first thing we get to execute is the ``perform`` instruction.
Here we see that it's asking us to perform the ``greet.hello`` effect,
and we just happen to have one in our current handlers list. So we
move on to running the code inside of that handler instead. Here
we show ``Hello!`` on the screen, and then continue executing from
where we "performed" the effect, but with the value ``1`` instead.
That is, it's as if we had replaced the "perform" instruction with ``1``::

    // Current handlers:
    on greet.hello() do
      show: "Hello!";
      continue with 1;
    end

    // Now running:
    let Result = 1;
    Result + 1;

And so we move on to the next expression, ``Result + 1``. Since
``Result`` is associated with ``1``, this gives us ``1 + 1``. The
final result of this entire ``handle`` block is, then, ``2``.


Continuations and returns
-------------------------

We've only glossed over the whole ``continue with`` business. Sadly,
the way handlers work is complicated and requires a more detailed
explanation.

Handlers and ``perform`` instructions work in tandem---as if they
were in a conversation. When we "perform", we ask a handler to take
over the execution of the program, and so we do as the handler
tells us to.

At any point, a handler may decide to give the stage back to the
perform instruction, giving it an "answer"---this is where the
``continue with`` expressions come in. This ``continue with``
expression is called a "continuation", and it knows exactly where
in the program we stopped---hence it can "continue" that execution
"with" some new value.

Most handlers will use the ``continue with`` expression to provide
some kind of answer to its ``perform`` counterpart. This is similar
to how values are returned in commands. That is, the following::

    handle
      let Result = perform greet.hello();
      Result + 1;
    with
      on greet.hello() do
        show: "Hello!";
        continue with 1;
      end
    end

Is similar to::

  command greet hello do
    show: "Hello!";
    1;
  end

  // And later:
  let Result = greet hello;
  Result + 1;

 
But instead of giving back an answer to the ``perform`` instructions,
handlers can also give back an answer *to the ``handle`` block itself*.
This is called a "return", and it looks like the following::

    handle
      let Result = perform greet.hello();
      show: "Here...";
      Result + 1;
    with
      on greet.hello() do
        show: "Hello!";
        return 1;
      end
    end

This works a bit different from our command execution. Instead of
putting the ``1`` back where the ``perform`` instruction was, the
``return`` instruction replaces the entire ``handle`` block with that
value. That is, we show ``Hello!`` on the screen, and then immediately
have the result of the entire block be 1. We'll never get to see
``Here...`` on the screen, because nothing else in that piece of code
will be executed.


Nesting handlers
----------------

Handlers can also be nested. For example::

    handle

      handle
        perform num.one() + perform num.two();
      with
        on num.one() do
          continue with 1;
        end
      end

    with
      on num.two() do
        continue with 2;
      end

      on num.one() do
        continue with 11;
      end
    end


Here the inner handle block only defines a handler for the ``num.one``
effect, which continues the program with 1. The outer handle block
defines a handler for ``num.two`` which continues the program with
2, and a handler for ``num.one`` which continues the program with
11.

So when we ``perform num.one()``, the inner handler is the closest
one, and we replace that perform instruction with 1. But when we
``perform num.two()``, there's no handler in the inner handle
block, so the closest one is the handler in the outer handle
block, which replaces the perform with 2. The result is then ``1 + 2``.

If the inner handle block did not have a handler for ``num.one``,
we would end up using the outer handler for it---ending up with
``11 + 2``.


Effect scoping
--------------

We've seen that bindings are valid within certain regions of the code---
which is their scope. Effects have a similar concept of being only valid
within a certain region, but the way these regions work is a bit different.

Bindings have a "lexical scope"---the region where they're valid can be
seen in the source code. But effects have "dynamic scope"---the region
where they're valid depends on how the program *runs*.

For example, consider the case where we have some commands that eventually
perform an effect::

    command show: Text =
      perform display.show(Text);

    command greet: Name =
      show: "Hello, [Name].";

Then if we have the following handle block::

    handle
      greet: "Alice";
    with
      on display.show(Text) do
        transcript display: Text;
        continue with nothing;
      end
    end

The handler is not restricted to the code that can be seen in
the handle block, but rather covers *all* code that is executed
from there. This means that, even though the perform only happens
in the ``show: _`` command, it still sees our little handler for
``display.show``, because it's called from ``greet: _``, which
is in turn called from within the ``handle`` block.

On the other hand, in the following example, the call to ``show: _`` that
arises from ``greet: "Dorothy"`` would not see the handler, because this
call does not originate from within the handle block::

    handle
      greet: "Alice";
    with
      on display.show(Text) do
        transcript display: Text;
        continue with nothing;
      end
    end
    greet: "Dorothy";


Missing handlers
----------------

What happens if we don't have a handler for a ``perform`` instruction?
Crochet will still execute the code as normal, but when hitting the
``perform`` instruction the program would stop.

In interactive mode, this means that you'd have a chance of deciding
how to continue the program, either by providing a value to continue
the program with, or by returning a value from the handle block.


Reusable handlers
-----------------

Handle blocks define how effects behave in the program, but defining
all of that behaviour in the handle block isn't feasible or desirable.
The package that defines the handle block might not even have access
to the effect, for security reasons. And even when it does, it can
easily lead to cases where the same handler code is repeated all over
the place, making the use of effects a chore.

To address these two problems, Crochet allows defining **reusable**
handlers. We can introduce one using the ``handler`` declaration::

    handler show-on-transcript with
      on display.show(Text) do
        transcript display: Text;
        continue with nothing;
      end
    end

We can then reference this handler within a handle block::

    handle
      greet: "Alice";
    with
      use show-on-transcript;
    end

Any number of ``use`` declarations can be mixed with ``on ...``
declarations in the handle block, but effects handled by the block
are not allowed to overlap. That is, it's not possible to have::

    handle
      greet: "Alice";
    with
      use show-on-transcript;
      on display.show(Text) => continue with nothing;
    end

Here both ``show-on-transcript`` and the inline handler are managing
the same ``display.show`` effect, so it's unclear which one Crochet
should use. That's thus disallowed.


Parameterised handlers
''''''''''''''''''''''

Consider the case where it's not entirely clear how a handler should
behave from its own perspective---it needs a bit more of context. For
example, when we display text, we might want to identify where that
text came from. Parameterisation allows the user of the handlers to
fill in this missing information.

Handler parameters are described in a similar way to command parameters::

    handler show-on-transcript chapter: (Chapter is text) with
      on display.show(Text) do
        transcript display: "([Chapter]) [Text]";
        continue with nothing;
      end
    end

We can use it like so::

    handle
      greet: "Alice";
    with
      use show-on-transcript chapter: "Prologue";
      on display.show(Text) => continue with nothing;
    end

With would result in the following output:

    (Prologue) Hello, Alice.

Note that, just like the commands ``greet: _`` and ``greet: _ from: _`` are
distinct, the parameterised handlers are also distinct. That is,
``show-on-transcript``, ``show-on-transcript chapter: _``, and
``show-on-transcript chapter: _ act: _`` would all be distinct handlers.


Handler initialisation
''''''''''''''''''''''

Another aspect of reusable handlers is that they may contain custom
initialisation code. That is, code that is executed before the ``handle``
block that contains it, and that may set up any necessary state for the
handler. This is often coupled with parameterised handlers to make the
internal state observable outside.

For example, a handler that collects text that uses ``display.show``
could be done as follows::

    type io(input is cell<list<text>>, output is cell<list<text>>);

    handler collect-show output: (IO is io) do
      let Output = IO.output;
    with
      on display.show(Text) do
        Output <- Output value append: Text;
        continue with nothing;
      end
    end

Initialisation code is executed before the handler is installed, so no
effects performed within it will be handled by the ``handle`` block 
that's using the handler. It is also executed in the sequence it appears
in the containing ``handle`` block, so ``use a; use b;`` would first
execute the initialisation code of ``a``, and then the initialisation
code of ``b``.


Default handlers
''''''''''''''''

For non-parameterised effects, it might be useful to install them
automatically at the global level. This allows pieces of functionality
to be redefined through handle blocks, but without imposing the use of
them on all programs, which might be useful in some cases.

Handlers can be marked as default like so::

    handler atomic-memory-cell with
      ...
    end

    default handler atomic-memory-cell;

Default handlers are installed before executing the application entry-point,
but **after** executing all prelude blocks. This means that preludes must
be inherently pure.