Foreign interfaces
==================

.. warning:: Crochet's FFI currently assumes trusted modules, and it'll
   most likely evolve into an Alien-based layer that allows a more nuanced
   view of security and permits safe sandboxing at a lower cost.

Sometimes Crochet does not provide enough to build the program 
you need. Maybe you have specific performance needs, or maybe
you want to use something that was built for another programming
platform. In these cases, Crochet offers a Foreign Interface mechanism
to interact with external programs.

Currently, foreign programs are limited to JavaScript.


.. toctree::

   interface
   ffi
   