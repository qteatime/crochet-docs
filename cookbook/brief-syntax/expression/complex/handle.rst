``handle`` expression
=====================

The handle expression introduces effect handlers to a piece of
code. It has the following syntax::

    handle
      Some;
      Expressions;
      Go;
      Here;
    with
      on some-effect.operation() do
        continue with "ok";
      end

      on some-effect.other-operation() do
        return "nope";
      end
    end

The do blocks may use the arrow form, which accepts a single complex
expression::

    handle
      Code;
    with
      on some-effect.operation() => continue with "ok";
    end

Additionally, it's possible to reference reusable handlers::

    handle
      Code;
    with
      use some-reusable-handler;
      use other-reusable-handler parameter: Argument;
    end


Example
-------

Continuations
'''''''''''''

Given the effect::

    effect increase with
      one(value is integer);
    end

We can write the following handle block::

    handle
      [
        perform increase.one(1),
        perform increase.one(2),
      ]
    with
      on increase.one(Value) do
        continue with Value + 1;
      end
    end

This will result in::

    [2, 3]


Returns
'''''''

Given the effect::

    effect non-local with
      result(Value);
    end

We can write the following handle block::

    let Items = [1, 2, 3, 4];

    handle
      for Item in self do
        transcript show: Item;
        perform non-local.result(Item);
      end
    with
      on non-local.result(Value) do
        return Value;
      end
    end

This will result in the transcript showing ``1``, and immediatelly
making that the result of the entire ``handle`` block, without
touching any of the other items.