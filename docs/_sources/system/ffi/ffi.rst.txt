The FFI type
------------

.. warning:: Crochet's FFI currently assumes trusted modules, and it'll
   most likely evolve into an Alien-based layer that allows a more nuanced
   view of security and permits safe sandboxing at a lower cost.

Native modules receive a single argument, an ``FFI`` object purposely
constructed for that package alone---which ensures that the interaction
between the VM and the native module are still bound to the same
capabilities that the package itself is.

Though, that said, until Crochet can sandbox JavaScript code, this
does not provide many guarantees.


Defining functions
''''''''''''''''''

.. js:method:: ffi.defun(name, fn)

   :param string name: The name of the foreign function.
   :param ((CrochetValue[]) => CrochetValue) fn: The foreign function implementation.

   Defines a simple, synchronous foreign function. The return must be a
   Crochet value.


.. js:method:: ffi.defmachine(name, machine)

   :param string name: The name of the foreign function.
   :param ((CrochetValue[]) => Generator(NativeSignal, CrochetValue, CrochetValue)) machine: The foreign function implementation.

   Defines a complex foreign function which can interact with the Crochet
   VM by yielding native signals (provided by this object). All intermediate
   values must be Crochet values.


Constructing Crochet data
'''''''''''''''''''''''''

.. js:method:: ffi.integer(x)

   :param bigint x: The number.

   Converts a JavaScript bigint value to a Crochet integer.


.. js:method:: ffi.float(x)

   :param number x: The number.

   Converts a JavaScript number value to a Crochet float.


.. js:method:: ffi.boolean(x)

   :param boolean x: The boolean.

   Converts a JavaScript boolean value to a Crochet boolean.


.. js:method:: ffi.text(x)

   :param string x: The text.

   Converts a JavaScript string to a Crochet text value. This always
   yields a dynamic text.


.. js:method:: ffi.box(x)

   :param x: The arbitrary value to box.

   Converts any JavaScript value to an opaque Crochet box. This box
   can be passed around in Crochet but never *opened* by Crochet code.
   It must be paired with :js:meth:`ffi.unbox` in order to extract and
   use its value.


.. js:method:: ffi.list(x)

   :param CrochetValue[] x: The list.

   Converts a JavaScript array to a Crochet list. The items of this
   array must already be Crochet values.


.. js:method:: ffi.record(x)

   :param Map(string, CrochetValue) x: The record.

   Converts a restricted JavaScript map to a Crochet record. All keys
   in the map must be strings, and all values must already be Crochet
   values.


.. js:method:: ffi.interpolation(x)

   :param CrochetValue[] x: The parts of the interpolation.

   Converts a list of interpolation parts to a Crochet interpolation.
   *All* parts of the interpolation will be dynamic.


.. js:method:: ffi.nothing()

   Returns the special ``nothing`` value.


.. js:method:: ffi.true()

   Returns the special ``true`` value.


.. js:method:: ffi.false()

   Returns the special ``false`` value.


.. js:method:: ffi.from_plain_native(x)

   Constructs a Crochet value from a plain JavaScript value, recursively.
   Note that this follows the same restrictions as the constructors above---records *must*
   be maps.


Using Crochet values
''''''''''''''''''''

.. js:method:: ffi.integer_to_bigint(x)

   Converts a Crochet integer to a JavaScript bigint.


.. js:method:: ffi.float_to_number(x)

   Converts a Crochet float to a JavaScript number.


.. js:method:: ffi.to_js_boolean(x)

   Converts a Crochet boolean to a JavaScript boolean.


.. js:method:: ffi.text_to_string(x)

   Converts a Crochet text (any trusted text) to a JavaScript string.


.. js:method:: ffi.list_to_array(x)

   Converts a Crochet list to a JavaScript array.


.. js:method:: ffi.interpolation_to_parts(x)

   Converts a Crochet interpolation to a list of parts. Literal parts in
   the interpolation are represented as JavaScript strings in the resulting
   array. Everything else is represented as a Crochet value.


.. js:method:: ffi.record_to_map(x)

   Converts a Crochet record to a JavaScript map.


.. js:method:: ffi.unbox(x)

   Takes the value out of a Crochet box. It's up to the caller of this
   function to verify that the value is indeed what they expect, type-wise.


.. js:method:: ffi.to_plain_native(x)

   Converts an arbitrary Crochet value to a plain JavaScript value, as if
   by one of the destructors above. Boxed values are not handled here. And
   records are always converted to JavaScript maps.


Native signals
''''''''''''''

.. js:method:: ffi.invoke(name, args)

   :param string name: The string representation of the command's signature.
   :param CrochetValue[] args: The arguments to provide the command.

   Returns a native signal that causes the VM to invoke the specified
   command with the native module's package's capabilities.


.. js:method:: ffi.apply(fn, args)

   :param CrochetValue fn: The Crochet delayed program to apply.
   :param CrochetValue[] args: The arguments to provide the delayed program with.

   Returns a native signal that causes the VM to apply a delayed Crochet
   program (lambdas or partials) to the given arguments.


.. js:method:: ffi.await(promise)

   :param Promise(CrochetValue) promise: The promise to wait for.

   Returns a native signal that causes the VM to wait the promise to be
   successfully settled before continuing the execution of the machine with its
   resolved value.


Operators
'''''''''

.. js:method:: ffi.intrinsic_equals(x, y)

   :param CrochetValue x:
   :param CrochetValue y:

   True if ``x`` and ``y`` are equal according to Crochet's intrinsic
   equality algorithm.


.. js:method:: ffi.panic(tag, message)

   :param string tag: A special mark to add to the panic message (e.g.: an unique name to the error).
   :param string message: The panic message.

   Stops the program with a panic message. This error cannot be caught in
   Crochet code.


Testing values
''''''''''''''

.. js:method:: ffi.is_crochet_value(x)

   True if ``x`` is a Crochet value.

