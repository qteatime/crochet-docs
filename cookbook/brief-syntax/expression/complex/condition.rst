``condition`` expression
========================

The condition expression allows one to execute the first piece of code
for which the corresponding condition is true. It has the following syntax::

    condition
      when X > 0 do
        "positive";
      end

      when X < 0 do
        "negative";
      end

      otherwise do
        "zero"
      end
    end

Do blocks may be alternatively written in the arrow form, which accepts
a single complex expression::

    condition
      when X > 0 => "positive";
      when X < 0 => "negative";
      otherwise => "zero";
    end

The ``otherwise`` fallback always succeeds (it's equivalent to ``when true``),
and must come at the end of list of conditions.