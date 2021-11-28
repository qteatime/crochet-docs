Projection
==========

Fields can be projected from records, objects, or lists through the
following syntax::

    Some-expression.field-name

Additionally, for records, keys whose names are not expressible as
a Crochet field name can be quoted::

    Some-expression."this is a record key"

Dynamic selection of record keys is also supported---where the key
is decided by evaluating an expression to some piece of text::

    Some-expression.(Key-expression)