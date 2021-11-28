``for`` expression
==================

The for expression allows one to do something with each item of
a collection. It has a few different forms.


Iteration form
--------------

The iteration form allows one to do something with each item of
a collection, in its defined order. It has the following syntax::

    let A = [1, 2, 3];

    for Item in A do
      A + 1;
    end

Which will produce::

    [2, 3, 4]

The ``Item`` part is a variable name that will refer to each item
of the collection in turn.


Filter form
-----------

The filter form allows one to exclude items from the iteration.
It has the following syntax::

    let A = [3, 6, 9];

    for Item in A if Item > 5 do
      Item + 1;
    end

Which will produce::

    [7, 10]


Nested form
-----------

The nested form allows one to do combine the iterations of different
collections. It has the following syntax::

    let A = [1, 2];
    let B = ["a", "b"];

    for Outer in A,
        Inner in B
    do
      [Outer, Inner]
    end

Which will produce::

    [
      [1, "a"],
      [1, "b"],
      [2, "a"],
      [2, "b"]
    ]