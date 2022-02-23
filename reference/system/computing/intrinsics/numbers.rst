Numeric models
==============

Dealing with numbers in a computer is tricky. The current version of
Crochet only offer support for a small part of this problem, which is
more likely to happen when writing interactive fiction. Future versions
will extend the numeric tower to cover other use cases, but do note that
Crochet is not designed for things like heavy numerical analysis or scientific
computing, so those spaces are unlikely to be covered in the standard library.

The numeric tower in Crochet has two types:

- **Integers**: the ``integer`` type can represent any integral number
  accurately, at the cost of computing power and memory to do so. That
  is, the further the number is from 0, the more memory is needed in
  order to represent it---and the more computing power is needed to
  perform arithmetic operations on it.

- **Floating points**: the ``float-64bit`` type is an approximation of
  fractional numbers that always consumes 64 bits of memory. It
  can accurately represent some integral numbers, and approximate
  some decimal numbers with varying degrees of precision.


Approximating fractionals
-------------------------

The ``float-64bit`` type follows the `IEEE-754 <https://en.wikipedia.org/wiki/IEEE_754>`_
specification, natively supported in hardware. Approximations always
consume 64 bits of memory, which means that integral numbers very far
from 0 and fractions are not going to be *accurately* represented in
the computer.

Operating on floats means that you're always operating on approximations,
and it's easy to lose precision, in particular when division operations
are involved.

Because games generally deal with *perceptual* values, rather than
*accurate* values, these approximations are usually not a big issue.
Efficiency and parsimonious use of memory are more important.


Mixed operations
----------------

Operations in Crochet can mix floating points and integers. For example,
the operation ``1 + 2.5`` is supported in Crochet. Whenever this happens,
the result of the operation will be promoted to the type that can best
approximate it. Currently, that means that any operation mixing floats
and integers will result in a floating point number---because integers
cannot approximate fractional numbers at all!
