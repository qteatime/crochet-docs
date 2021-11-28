Record expressions
==================

A record expression constructs a record from a sequence of key/value
pairs. If all key/value pairs are atomic, then the record itself is
also atomic.

An empty record has the following syntax::

    [->]

A record with pairs in it has the following syntax::

    [
      some-key -> Some-expression,
      "some other key" -> Some-other-expression,
      (Key-expression) -> Another-expression,
    ]

The sequence of pairs can have a trailing comma, but it's not required.