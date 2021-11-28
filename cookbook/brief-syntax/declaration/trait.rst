``trait``
=========

A trait declaration specifies a set of command requirements, and possibly
needs to implement other traits. It has the following syntax::

    trait some-name with
      requires trait trait-name;

      command _ === _;
    end

It can be preceded by a documentation comment::

    /// Some documentation comment
    /// Goes here
    trait some-name with

    end


Trait requirements
------------------

Trait requirements can be specified with the ``requires trait`` syntax.
The traits may come from other packages::

    requires some-trait-name;


Command requirements
--------------------

Commands required to be implemented by types implementing the trait
use the same syntax as the Command Declaration, but without an
implementation or test block::

    command _ === _;

    command A and B
      requires commutative :: (A and B) === (B and A);

Commands requirements may be preceded with a documentation comment::

    /// Some documentation of the requirements
    command _ === _;