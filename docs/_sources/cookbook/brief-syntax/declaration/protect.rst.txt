``protect``
===========

Protect declarations can apply to definitions, effects, types, and traits.
It does not accept any preceding documentation comments. The entity and the
capability must be defined by the package using this declaration.


Definitions
-----------

::

    protect global some-name with some-capability-name;


Effects
-------

::

    protect effect some-name with some-capability-name;


Traits
------

::

    protect trait some-name with some-capability-name;


Types
-----

::

    protect type some-name with some-capability-name;

