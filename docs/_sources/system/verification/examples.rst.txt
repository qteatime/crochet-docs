Example-based testing
=====================

The simplest form of verification in Crochet is the use of examples.
In this form one has a specific scenario of the program in mind,
and then verifies that the program behaves in that specific way.
Examples are used for verifying small pieces of the program,
rather than the entire program. And this process is generally
called "unit testing".


Test declarations
-----------------

Crochet's support for example testing comes in the form of
test declarations. Each of these test declarations can cover
one of these scenarios, and verifications are done with the
``assert`` expression.

For example, consider the case where we have a command to
display the list of items in an inventory with your usual
English conjunctions. An example test for it could look
like the following::

    test "inventory display with conjunctions" do
      assert (#inventory with: [] | show) === "You're not carrying anything.";

      assert (#inventory with: [rose] | show) === "You're carrying [rose].";

      assert (#inventory with: [rose, watch, old-coin] | show)
        === "You're carrying [rose], [watch], and [old-coin].";
    end

Here we have three different ``assert`` expressions that verify
different possibilities of displaying an inventory. When one isn't
carrying anything, "You're not carrying anything." should be displayed.
But when they're carrying multiple items, we'd expect something
more along the lines of "You're carrying a rose, a watch, and an old coin.".


Convenience for command tests
'''''''''''''''''''''''''''''

Though you can always use the test declaration syntax, there's a slightly
more convenient syntax for describing examples for a single command.
Instead of writing the separated test declaration, as above, we could
have added a test block to the ``inventory show: _`` command itself::

    command inventory show do
      condition
        when self.items is-empty => ...;
        when self.items size === 1 => ...;
        otherwise => ...;
      end

    test
      assert (#inventory with: [] | show) === "You're not carrying anything.";

      assert (#inventory with: [rose] | show) === "You're carrying [rose].";

      assert (#inventory with: [rose, watch, old-coin] | show)
        === "You're carrying [rose], [watch], and [old-coin].";    
    end

This convenience syntax works exactly like the separated test declaration,
but it uses the name of the command as a description.


Testing effects
---------------

.. warning:: Effectful testing is still in discovery; this section will be
   expanded in the future.

When the pieces of program you want to test only depend on the data
you're using, your examples will consist of constructing the data,
executing a command, and then comparing the resulting data with
what you expected to happen.

But testing programs that have effects requires more sophisticated
examples. And that's because effects usually do things outside
of what can be reasonably verified in Crochet. So one approach to
testing these programs is to use a handler that, instead of
doing things outside of Crochet, just keeps track of what was
supposed to happen. The examples may then verify that what was
supposed to happen in the program really matches what the program
should be doing.
