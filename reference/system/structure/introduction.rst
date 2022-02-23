The Crochet universe
====================

What are Crochet programs made out of? Well, many things, it turns out.
First, Crochet programs are organised into packages. These packages will
then dictate what other packages they need in order to work, as well as
how much it trusts each of these packages. And packages will also contain
modules---this is where we start getting deeper into "code".

Modules are a collection of "code entities". They may contain types,
definitions, commands, tests, as well as several other less common things:
relations, capabilities, actions, events, patches, and so on.

An application written in Crochet will usually be made out of several
different packages---which in turn will have several modules, containing
several code entities. But there isn't really a technical distinction
between "package" and "application" in Crochet. An application _is_ a
package. The "root" package, to be more precise. It's from there that
Crochet decides what to load, and how much "power" each of the loaded
packages should have.

If this sounds confusing, don't worry. We'll see this in more details,
and with more examples.


Packages
--------

A package is the highest level of organisation in Crochet. A package
can be your application, but more often than not, a package is a
component---like a matching block---which you can combine with other
packages to build bigger things.

They exist as a directory in your computer's file system, and must
contain at least one file called ``crochet.json``. This file is what
tells Crochet what the package is all about. But a package will also
contain other files: modules, documentation, images, etc. The ``crochet.json``
file aside, these can be organised freely inside of the directory---conventions
exist, but they're just conventions.


``crochet.json``
''''''''''''''''

So what's this ``crochet.json`` file anyway? It's a `JSON <https://en.wikipedia.org/wiki/JSON>`_ 
file that describes what the package is, what it uses, and what it contains.
We call it, more colloquially, the :ref:`Package Configuration <package-configuration>`.

The package configuration also tells Crochet where to find the things a package
contains, as again Crochet doesn't force items to be organised in any particular way.

This file might look like the following:

.. code-block:: json

   {
     "name": "my-package",
     "description": "A really cute package for Crochet",
     "target": "browser",
     "dependencies": [
       "crochet.core"
     ],
     "sources": [
       "my-module.crochet"
     ]
   }

So this tells us that we have a package called ``my-package``. It only works
in the web browser. It uses another package called ``crochet.core`` (which
is distributed with Crochet). And it contains a single module, which can
be found in the file ``my-module.crochet``, in the same folder as the JSON
file.

We go into more details on what exactly all of these properties---like ``"name"``
or ``"target"``---in the JSON file mean, and how one would go about reading
and writing these files in the :ref:`Package Configuration <package-configuration>` section.


Directory structure convention
''''''''''''''''''''''''''''''

Crochet isn't picky at all about how you decide to structure your files---you
will be describing that in your package configuration. However, there is a
convention for organising them. By following the convention, you can make
the life of people who're using your package easier, if they want to
learn from it or modify it.

So packages generally look like the following (directories are described with
a ``/`` (forward slash) after their name):

.. code-block:: text

   o my-package/                      (this is the package directory)
   |
   |---o crochet.json                 (the package configuration)
   |---o source/                      (modules will be placed here)
   |   |
   |   `---o my-module.crochet
   |
   |---o native/                      (native modules will be placed here)
   |---o test/                        (additional tests will be placed here)
   `---o assets/                      (images, sounds, etc. will go here)


Modules
-------

So packages will contain modules. But what in the world are modules anyway?
Well, they are files that tell Crochet what *code* makes up the package.
Things are a bit trickier here than in other programming systems you may
be familiar with because Crochet is a "language-driven" system. What this
means is that modules may (and *will*) be written in different programming
languages.

For example, our ``my-module.crochet`` file from before could look like
the following::

    % crochet

    define greeting = "Hello";

    command greet: Person = "[greeting], [Person]!";

This module provides two code entities: the definition ``greeting``, and
the command ``greet: Person``. Don't worry about what these mean for now.
We'll see all of this in more details later. The important thing to note
here is that modules are, essentially, a collection of these "code entities".
So the code that a package contains will be all of these modules' code entities
combined.

But modules are not aways these ``.crochet`` files---because Crochet is
language-driven, modules can be written in many different languages, and not
just the Crochet language. For example, the following ``arithmetic.lingua``
is also a module, ready to be included in a package and loaded as code::

    % lingua

    type Arithmetic =
      | Addition(left: Arithmetic, right: Arithmetic)
      | Subtraction(left: Arithmetic, right: Arithmetic)
      | Number(value: Text)

    grammar Arithmetic : Arithmetic {
      Expression =
        | left:Expression "+" right:Expression  -> Arithmetic.Addition(left, right)
        | left:Expression "-" right:Expression  -> Arithmetic.Subtraction(left, right)
        | value:number                          -> Arithmetic.Number(value)

      token number = digit+
    }

It looks nothing like our ``my-module.crochet`` because it's written in the
Lingua language, rather than the Crochet language. But the Crochet *system*
is able to load this code just as well as the Crochet one. The idea in Crochet
is that each module is written in the language that makes the most sense
for the task it's solving---and the Crochet system will make sure they
can all be combined into a single package (and application), by automatically
translating between the new language (like Lingua) and the Crochet language.


Code entities
-------------

So modules are a collection of these "code entities". But what exactly are
"code entities" anyway? They're specific concepts that the Crochet knows
how to interpret in order to make the computer behave in particular ways.
They provide definitions and rules that direct computers, in a sense.

Collectively, these entities make up the "code" portion of a package, and
they are further divided into many types of entities.


Types
'''''

A type tells Crochet how to classify and structure some piece of information.
They also play a key role in Crochet's security and privacy guarantees. Here,
a type is an unique, unforgeable name that has some structure associated with
it.

For example::

    type rectangle(width, height);

This type has the name ``rectangle``, and contains two pieces of information:
the ``width`` of the rectangle, and the ``height`` of the rectangle. These
pieces are also called Fields. We discuss types and their usage in more details
in the :ref:`Data and Types <data-and-types>` chapter.

But how are names unique? And what exactly does it mean for names to be
"unforgeable"? We discuss these in details, and what exactly these properties
mean for Crochet's security guarantees, in the Security chapter.


Commands
''''''''

A command tells Crochet how to compute---how to instruct the computer to
do something. Not only that, but commands are the *only* way to instruct
the computer to do something. Nothing happens in Crochet if not by the
execution of a command---and this has some important security and usability
implications that we'll discuss in the Interactive Programming chapter.

Commands look like this::

    command (X is rectangle) area = X.width * X.height;

This can be read as: "understand the area of a rectangle (we'll call it X),
as the width of X times the height of X." It describes a rule to Crochet, and
this rule tells Crochet how the area of a rectangle is computed.

The name of this command is not really ``area`` though, but rather ``_ area``.
The underscore (``_``) is used by convention to show where the arguments for
that command should go. In the body of this command, ``*`` is just another
command! More specifically, the ``_ * _`` command. Notice how ``X.width`` and
``X.height`` both fill the underscore spaces---the way you define a command
is very similar to the way you use it.

Unlike types, multiple commands with the same name can exist in Crochet, as
long as they apply to different types---in the example above, the ``is rectangle``
part is what tells us what types the command applies to. So we could have, in
the same module or elsewhere, something like::

    command (X is circle) area = (X.radius ** 2) * pi;

Because Crochet knows what type is associated with each piece of information,
whenever we ask "hey, what's the ``_ area`` of this thing?", Crochet will know
exactly which command needs to be executed, even though multiple rules for
``_ area`` exist.

We discuss commands and their usage in more details in the :ref:`Commands <commands>`
chapter.


Traits
''''''

If a type classifies one piece of information, then a trait identifies common
aspects of many types. This commonality is, in Crochet, mostly captured by
commands that can be performed on different types.

For example, rectangles and circles are different kinds of shapes.
But they both have a concept of an ``area``. This commonality can
be captured with a trait::

    trait has-area with
      command X area;
    end

    type rectangle(width, height);
    type circle(radius);

    implement has-area for rectangle;
    command (X is rectangle) area = X.width * X.height;

    implement has-area for circle;
    command (X is circle) area = (X.radius ** 2) * pi;

Here we define a trait called ``has-area``, and the requirement for it is
that the type must understand a ``_ area`` command. But just defining an
``_ area`` command isn't sufficient---we also need to be explicit about
wanting the type to belong to this trait. That's what we're doing with
the ``implement has-area for ...`` entities.

Why be explicit about it, though? Isn't it obvious that rectangle and
circle have an area? Well, it might seem so because we're the ones defining
it. But when we're dealing with other packages---which might not even be
aware of traits we've conjured!---, it's easy to get into situations where
types fulfill all of the requirements from a trait, but the commands don't
really *behave* as we expected.

If someone defines a type ``game-map``, and gives it an ``_ area`` command
that provides the current area the player character is in, should ``game-map``
really belong to our ``has-area`` classification for geometric shapes? Quite
unlikely.

We discuss more about traits, including how and when to use them, in the
:ref:`Data and Types <data-and-types>` chapter.


Effects and Handlers
''''''''''''''''''''

Many programming systems try to make it easier to show things on the screen
or interact with files. After all, what good is a program if you can't see
what it's doing? Surely a program is only as good as the effects it has?

Well, Crochet takes a different approach. By default, no programs can show
things on the screen, interact with files, or, really, do anything that someone
would be able to observe. And there's a very good reason for this: all of these
things have a big impact on the security guarantees we can provide, and they
can have very disastrous results: imagine writing a program to delete files
and only realising you'd deleted the wrong one after it's gone!

So, in Crochet, one describes what they expect the system to do---e.g.: showing
things on screen, or deleting files. But how these things are carried out is
decided later, and can very well be replaced. For example::

    effect display with
      show(text);
    end

Here we tell Crochet that we have some intention of showing text on the screen,
and later we can ask Crochet to do so by performing this: ``perform display.show("Hello")``.
But *how* Crochet actually goes about performing it is defined elsewhere,
through handlers:

    handler show-on-transcript with
      on display.show(Text) do
        transcript show: Text;
        continue with nothing;
      end
    end

Effects are certainly one of the more difficult parts of Crochet. And so they
get their own chapter, which explains, in depth, why they're important, how
they're used, and why they are the way they are.


Capability groups
'''''''''''''''''

Capabilities are how Crochet is able to guarantee that programs can be safe
even if you add code from the internet to it. They also allow one to reason
about a program---and then decide whether you trust it or not.

A capability group is an entity that describes some kind of power---or
capability. For example, we might think that deleting files is a dangerous
thing. What if someone sends you a Crochet package, telling you they'd love
if you could help beta-testing their new game, and then you run it, and
it deletes all of your personal photos. That wouldn't be cool.

If, instead, we have a capability for deleting files, then Crochet would
tell you beforehand: "Hey, this game you're running can actually delete
your files. Do you want to run it anyway?".

For example::

    capability delete-files;
    type file-system;
    protect file-system with delete-files;

Here we do three things: tell Crochet that "deleting files" is a thing, and
is a very dangerous thing. We then introduce a ``file-system`` type, and tell
Crochet that by using ``file-system`` one would be able to delete files. This
way Crochet can accurately track these dangers and only show you *relevant*
ones.

Of course, it's not just because something can do dangerous things that it is
inherently evil---but we discuss what exactly it means, and what goes into
deciding whether to trust some application or not in the Security chapter.


Tests
'''''

Tests are an important part of developing any software. Crochet supports
tests as just any other code entity, and provides tools for running them.

They look like this::

    test "Addition" do
      assert (0 + 1) === 1;
      assert (1 + 0) === 1;
      assert (2 + 3) === 5;
    end

We discuss testing and Crochet's support for tests in the Testing chapter.


Native modules
--------------

So, the Crochet system only speaks the Crochet language natively. Sadly,
the Crochet language is very limited. For example, it doesn't even have any
concept of arithmetic addition! Let alone a concept of drawing things on
a screen.

How exactly do Crochet applications get to do anything? That is, if
I can write ``2 + 3`` in Crochet and get ``5`` as a response, how exactly
does Crochet know what to do there, if it doesn't know what an arithmetic
addition is?

Well, someone needs to teach Crochet what to do in these cases. These missing
concepts are often added to Crochet by using a different language---a language
that the computer speaks natively. That's the role of a Native Module. Instead
of being restricted by what Crochet can do, they are restricted by what the
native language can do. Most native modules in Crochet are written in
`JavaScript <https://en.wikipedia.org/wiki/JavaScript>`_.

Because native modules aren't restricted by Crochet's rules and limitations,
they are *very powerful*. And all of this power is dangerous. In order to
make Crochet safe for everyone, the use of native modules is carefully
controlled through Capabilities.