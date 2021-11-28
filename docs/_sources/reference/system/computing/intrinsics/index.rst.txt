Intrinsic data types
====================

Crochet includes, out of the box, a collection of basic types---called
intrinsics. These types are useful for most Crochet applications, but
they also define a baseline for some of the security guarantees that
Crochet provides. Without these it would be very difficult to make
Crochet safe.

The intrinsic types cover the following categories of problems:

- **Numeric models**: these types represent different forms of numbers,
  only somewhat similar to what you'd see in mathematics as we still
  need to deal with some peculiarities of digital representation and
  computer resources.

- **Textual models**: these types provide a way of representing and
  combining arbitrary pieces of text, securely. This turns out to be
  a much more difficult problem than one may think at first, so we
  spend a lot of time in the details of these textual types---and
  both technical and sociological implications, too.

- **Gradual representations**: we don't always know what kind of
  data we're dealing with---or if we're dealing with a piece of
  data at all. Crochet explicitly captures this and allows different
  pieces of code to have varying amounts of knowledge about what
  data they're handling. This turns out to be very important for
  security in some situations!

- **Logical models**: we need to represent answers to questions
  like "is the door locked?", and both philosophy and mathematics have
  given us different models for this. Crochet exposes a very simple
  one as an intrinsic type. We also discuss why, when, and how you might
  reach out for other models.

- **Program representations**: we need to represent partial and
  delayed programs. In Crochet these end up as either Functions or
  Thunks.

- **Collections**: somestimes we need to talk about several values
  in a consistent way. Collections are one way to achieve that.


.. toctree::
  
   gradual
   numbers
   text
   logic
   functions
   collections