Interpolation
=============

Interpolation allows constructing values that mix pieces of
literal text with other values. They are atomic only as long
as **all** of their dynamic pieces are also atomic.

They have the following syntax::

    "Some piece of text [Some-expression] and [Another-expression]"