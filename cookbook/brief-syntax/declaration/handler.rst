``handler``
===========

Reusable handlers allow defining a set of effect handlers that can be
included elsewhere::

    handler ignore-io with
      on io.write(Text) => continue with nothing;
      on io.read(Text) => continue with "Placeholder";
    end

With a handle block we can use this as::

    handle
      let Name = io read;
      io write: "Hello, [Name]";
    with
      use ignore-io;
    end

These handlers can also be parameterised and include initialisation code::

    type io(input is cell<list<text>>, output is cell<list<text>>);

    handler capture-io io: (IO is io) do
      let Input = IO.input;
      let Output = IO.output;
    with
      on io.write(Text) do
        Output <- Output value append: Text;
        continue with nothing;
      end

      on io.read() do
        let Value = Input value first;
        Input <- Input value rest;
        continue with Value;
      end
    end

A handler can be automatically installed in the program by marking it as
default. This causes all code to use this handler, unless a more specific
handle block redefines its handled effects::

    default handler ignore-io;
