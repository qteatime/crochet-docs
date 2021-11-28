``return`` expression
=====================

In contracts
------------

Within a contract's post-condition, the ``return`` expression will refer to
the value that was returned by the command. It has the following syntax::

    command A successor
    ensures bigger :: return > A
    do
      // Implementation
    end


In effect handlers
------------------

Within an effect handler, the ``return`` expression will return a value from
the enclosing ``handle .. with .. end`` block. It has the following syntax::

    return Some-expression

The expression is always required in this case.