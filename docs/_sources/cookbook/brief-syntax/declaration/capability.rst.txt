``capability``
==============

A capability declaration introduces a new capability in the package.
It has the following syntax::

    capability some-capability-name;

It accepts a preceding documentation comment with the syntax::

    /// Some documentation comment
    /// Which may also have multiple lines
    capability some-capability-name;


Example
-------

::

    capability too-powerful-handle-with-care;

    type fluff-fiction;
    protect type fluff-fiction with too-powerful-handle-with-care;