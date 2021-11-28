``local``
=========

A local declaration can modify definitions, types, traits, and effects to
be visible only within the module that declares them. It accepts preceding
documentation comments.


Definitions
-----------

::

    local define some-name = Atomic-expression;


Types
-----

::

    local type some-name;


Traits
------

::

    local trait some-name with
      command _ + _;
    end


Effects
-------

::

    local effect some-name with
      operation();
    end