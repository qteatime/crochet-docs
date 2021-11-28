``effect``
==========

An effect may be declared with the following syntax::

    effect my-effect with
      operation();
      operation-with-parameters(one, two, three);
    end

It may be preceded by a documentation comment::

    /// Documentation comment
    /// With multiple lines
    effect my-effect with

    end


Parameters
----------

Parameter constraints are the same as Commands Requirements.