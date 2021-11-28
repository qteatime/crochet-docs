``do .. end`` expression
------------------------

A ``do .. end`` expression allows one to put a sequence of statements where
a complex expression is expected. The last statement's result
becomes the result of the do expression. It has the following syntax::

    do
      let A = 1;
      let B = 2;
      A + B;
    end