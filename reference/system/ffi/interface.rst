Writing external functions
==========================

.. warning:: Crochet's FFI currently assumes trusted modules, and it'll
   most likely evolve into an Alien-based layer that allows a more nuanced
   view of security and permits safe sandboxing at a lower cost.

The core idea of Crochet's foreign interfaces is to be able to
define functions in a separate language, and then execute those
functions from Crochet code. Currently the only supported language
is JavaScript.


Native modules
--------------

Foreign functions are written in "native modules", and are loaded
by specifying them in the package configuration. A JavaScript native
module has the following form:

.. code-block:: javascript

   exports.default = (ffi) => {
     // native function definitions go here
   }

Within that exported function, the native module can either specify
simple synchronous functions---through the ``ffi.defun`` method---,
or complex asynchronous functions---through the ``ffi.defmachine`` method.
A synchronous function here is simply one that just takes some arguments,
does something, and then returns a result.

For example, a native counter could be written as follows:

.. code-block:: javascript

   exports.default = (ffi) => {
     class Counter {
       #value;

       constructor(value) {
         this.#value = value;
       }

       next() {
         return new Counter(this.#value + 1n);
       }

       value() {
         return this.#value;
       }
     }

     ffi.defun("make-counter", (initial_value0) => {
       const initial_value = ffi.integer_to_bigint(initial_value0);
       const counter = new Counter(initial_value);
       return ffi.box(counter);
     })

     ffi.defun("next", (counter0) => {
       const counter = ffi.unbox(counter0);
       if (!(counter instanceof Counter)) {
        throw ffi.panic("invalid-type", "expected Counter");
      }
       return ffi.box(counter.next());
     })

     ffi.defun("value", (counter0) => {
       const counter = ffi.unbox(counter0);
       if (!(counter instanceof Counter)) {
         throw ffi.panic("invalid-type", "expected Counter");
       }
       return ffi.integer(counter.value());
     })
   }

It could then be used in Crochet as follows::

    type counter(box);

    command #counter with: (Value is integer) =
      foreign make-counter(Value);

    command counter next =
      foreign next(self);

    command counter value =
      foreign value(self);

The names defind by the native module are only valid within
the package loading it, so there's no chance of unexpected
collisions. However, it's still possible to use dots (``.``)
in the name---e.g.: ``counter.next`` would be a valid foreign
function name. These dots don't have any special meaning, but
it can make names easier to follow in packages that use a
significant amount of foreign functions.


``defun`` and ``defmachine``
----------------------------

Functions can be defined with both ``defun`` and ``defmachine``.
One could see ``defun`` as a simplified form of ``defmachine``,
but ``defun`` has different performance characteristics as well.

When using ``defun``, the function being called takes over the
execution for as long as it takes to return a value to Crochet,
and it isn't allowed to execute any Crochet code. This lets
us not bother with having stack frames for native code, which
is significantly cheaper, however it does mean that the Crochet
VM is paused for the duration of the function being executed;
it's only really suitable for functions that finish quickly.

When using ``defmachine``, we provide a JavaScript generator
to Crochet. This generator allows us to coordinate with
Crochet code and do asynchronous things, but it also means
that we need to allocate and deal with mixed Crochet and
native frames in the execution stack---this complexity has
a price that can't be entirely removed.

One use case for ``defmachine`` is to interact with JavaScript
promises, which are asynchronous. For example, a native
function that fetches data from the network could look
like the following:

.. code-block:: javascript

   async function fetch_text(url) {
     const response = await fetch(url);
     const text = await response.text();
     return ffi.text(text);
   }

   ffi.defmachine("fetch", function* (url) {
     const text = yield ffi.await(fetch_text(url));
     return text;
   })

The ``ffi.await`` function produces a signal that lets the Crochet VM
resume the current generator once the promise settles. And we send this
signal to the VM by ``yield``-ing it. In this sense, the VM runs the
generator step-by-step. At each step, the generator can yield a signal
that causes the VM to perform some work. And it finishes by returning
a value.

Now, the important thing to remember here is that **all** intermediate
values have to be Crochet values---not JavaScript ones. That's why we
abstract ``fecth`` into a ``fetch_text`` function, which ensures that
the promise will be resolved with a Crochet data structure.


