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
We call it, more colloquially, the Package Configuration.

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
and writing these files in the Package Configuration section.


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
Well, they are files that tell Crochet what _code_ makes up the package.
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