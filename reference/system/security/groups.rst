Capabilities and groups
=======================

Capabilities are little unforgeable keys that can be given to some
piece of code to enable it to perform something specific. In this
section we dive into details of how these little keys work in Crochet.


Primordial capabilities
-----------------------

Just like mobile phones have a set of capabilities of themselves that can be
given to any application---like "camera access"---, Crochet has a set of
capabilities of itself that can be given to any package. Crochet calls them
"primordial capabilities"---because they exist for as long as Crochet itself
exists, even if no packages were to be brought into existence.

There is currently only one primordial capability in Crochet:

- ``native``: a package with the ``native`` capability is allowed to
  define modules using the Foreign Interface. Such modules cannot be
  properly contained by Crochet, and thus threaten all of the security
  guarantees that Crochet aims to provide; but, sometimes, they're necessary.
  This is why Crochet allows one to give permission to a package to do
  such dangerous thing, by granting it the ``native`` capability.


Types as capabilities
---------------------

In Crochet, types also play the role of capabilities. This is a bit different
from how capability security appears in other programming languages, but
it supports Crochet's idea of supporting people to reason about what
kind of risks they're taking, and who they're taking risks with.

A type is an unique, unforgeable name. The powers a type grants are
access to the commands which have them as requirements. This allows
us to think about risks both in the higher-level sense of the type
itself, and in the more fine-grained sense of individual commands.

In order to make sure that people are only taking the risks
they're comfortable with, Crochet needs to make sure that these
types are only known by some pieces of code. This is achieved by
restricting types to their declaring package.


Granting type capabilities
''''''''''''''''''''''''''

If package A declares a type ``some-power``, then only package A has
access to it initially. No other package can have A's ``some-power``---no
other package can get that specific power. This is the "unforgeable" guarantee.
It's not enough to *know* the name of a type---you need to be given
access to it in order to use it.

For example, if capabilities were keys that can open very specific locks,
then it wouldn't be enough to just know what the key looks like---its colour,
shape, size. You would need to get your hands into the physical key in order
to open those locks.

This process is what Crochet refers to as "capability grants". Crochet itself
manages this "granting" part---the act of getting the "physical" keys into
the hands of specific pieces of code. And the default process of granting
capabilities is that the package which has declared a type has a grant to
use that type---but no other package will have the same grant.

Still, in order for packages to cooperate, sometimes we need to share these
keys with others. One way to do this is through package dependencies. A
package may request access to the types of another package by declaring
that it depends on it in order to work.

For example, the following Package configuration would request access to
the types of package ``crochet.random``:

.. code-block:: json

   {
     "name": "my-package",
     "dependencies": [
       "crochet.random"
     ]
   }

This allows ``my-package`` to use types such as ``crochet.random/random``,
either by referring to it through its full name, or by opening the package
first::

    open crochet.random;

    // Then later
    let Random = #random with-seed: 123456789;

But if what if we had a different package, ``other-package``, which did
*not* have a dependency on ``crochet.random`` in its package configuration?
Surely it knows what the full name of the ``random`` type is, so it could
try to have code that looks like this::

    let Random = #crochet.random/random with-seed: 123456789;

But if we run this, we'll get the following error message from Crochet's
security policy:

    **lacking-capability**: Accessing type random cannot be done
    in module ``test`` in ``other-package`` because the package
    does not have the following required capabilities:
    a dependency on ``crochet.random``.


Capability groups
-----------------

If primordial capabilities are those defined by Crochet itself, then
capability groups are the similar concept for things package developers
come up with---capabilities that are defined by the package itself.

A capability group is a way of declaring a dangerous power, and also
what exactly are the risks that this power carries---what Crochet should
make sure to not let users access without understanding and consenting
to these risks.

A group is introduced with the ``capability`` declaration::

    capability too-powerful;

If ``my-package`` has the declaration above, then we would let Crochet
know that a capability ``my-package/too-powerful`` exists. But just
declaring a capability is not entirely meaningful, we also need to
declare what exactly this capability means---what Crochet must protect
with this capability. That's done through the ``protect`` declaration.

For example, if this package were to define the type ``game-state``,
which allows one to create, load, and delete save files, it might 
want to tell Crochet that such type is powerful::

    type game-state;

    protect type game-state with too-powerful;

Additionally, the ``protect effect`` and ``protect global`` forms
of this declaration exist for Effects and Global Bindings respectively.

Finally, if a package wants to share this capability with others,
it must tell Crochet so in its package configuration:

.. code-block:: json

   {
     "name": "my-package",
     "modules": [],
     "capabilities": {
       "requires": [],
       "provides": [
         {
           "name": "too-powerful",
           "description": "Allows creating, loading, and deleting save data."
         }
       ]
     }
   }

Capability groups can be entirely internal, too! In that case, the capability
group is used to tell Crochet that a set of types, effects, and global bindings
are too powerful, and no other package will ever be able to access them. That
power is then entirely restricted to its defining package.


The ``internal`` capability
'''''''''''''''''''''''''''

It's often desirable to keep some definitions contained within its declaring
package, by default. In Crochet, all packages get an intrinsic ``internal``
capability to achieve this.

For example, it may be desirable to keep secret seals internal::

    define seal = lazy (#secret-seal description: "internal seal");
    protect global seal with internal;

That way we can ensure that only code within this package has the ability
of creating and reading its own secret pieces of data.


Propagating capabilities
------------------------

So, if capabilities are like physical keys that we can give to pieces
of code to allow them to do things, *who* is out there giving out these
keys?

Well, everyone is. Yes, everyone. Not just Crochet. And that's what makes
this process a bit complicated. In order to make this process safe, Crochet
needs to supervise it.

The process of granting---and propagating---capabilities involves a few
concepts:

- The capabilities are **unforgeable**. That is, in order to use a
  capability---in order to use this key---you need to be given the key
  by someone. You cannot just *materialise* a key out of thin air with
  wishes and knowledge alone.

- You can **choose to share** a capability that you're given with
  another package that you trust. This package is then one of your
  dependencies. But you have to *actively* choose it. By default
  Crochet does not share any capabilities with anyone.

- Once you share a capability, you cannot go back on your word. Capabilities
  are **irrevocable**, when shared in this manner. But that's only because
  we want to be able to *think* about what exactly we're trusting. Crochet
  allows a different way of granting capabilities that allows us to take
  back the key, which we'll cover in the next chapter.

In terms of how this all works in practice, a package must declare in
its ``required`` capabilities any key that it needs in order to work.
And in its dependencies, it must *provide* any capability that it wishes
to share. For example, consider the following package configuration:

.. code-block:: json

   {
     "name": "my-game",
     "dependencies": [
       {
         "name": "save-data",
         "capabilities": ["simple-save-data/save-data"]
       },
       {
         "name": "crochet.random",
         "capabilities": []
       }
     ],
     "capabilities": [
       "requires": [
         "crochet.random/read-shared-instance",
         "simple-save-data/save-data"
       ],
       "provides": []
     ]
   }

Here, the ``my-game`` package needs to be provided with the
``crochet.random/read-shared-instance`` and ``simple-save-data/save-data``
capabilities in order to work. Once it's loaded---and given those keys---it
then proceeds to load the ``save-data`` package. Now it has two keys that
it could share, but it only chooses to share the ``simple-save-data/save-data``
key.

*Even if* the ``save-data`` package chooses to, later on, use the
``crochet.random/read-shared-instance`` capability, it cannot do so because
``my-game`` chose to not share that key. This is how we can be absolutely
certain that ``save-data`` will never be able to do anything that isn't
interacting with save data. It will never be able to interfere with the
random number generator that is used by ``my-game`` because it simply
does not have that key. It can't get access to the types and bindings
it would need to do so.

But how does ``my-game`` gets its hands on those keys anyway? Well, if
``my-game`` is loaded as the dependency of another package, it's up to
that package to give ``my-game`` the capabilities it needs. But at some
point, someone really needs to "fabricate" these keys---at the top level,
that "someone" is Crochet. When a user runs a Crochet application---which
is really a Crochet package---it'll be asked to share with the application
all of the capabilities it needs, and if the user agrees to do so, Crochet
will fabricate those keys and pass it on to the application. The application
can then choose to share as many or as few keys as it wants, depending on
its needs and on how much it trusts its dependencies.


A note on cycles
''''''''''''''''

When we put all of these dependencies together, Crochet expects them
to form a tree---or, rather, an acyclic graph. That is, a package
cannot depend on something that will eventually contain itself as
a dependency. Crochet would never be able to figure out who's
granting powers to who in that case.

For example, consider the following dependencies:

- ``alice`` depends on ``bob`` and ``teresa``;
- ``bob`` depends on ``clara`` and ``kim``;
- ``kim`` depends on ``teresa``;
- ``clara`` and ``teresa`` do not depend on anyone.

We could visualise this as the following:

.. code-block:: text

   alice
     |
     |
     `---+------------,
         |            |
         V            V
        bob         teresa <-----,
         |                       |
         |                       |
         `---+--------,          |
             |        |          |
             V        V          |
           clara     kim         |
                      |          |
                      |          |
                      `----------'

Note how, if we follow the arrows in this graph, regardless of the path
we take, if we see one of these packages once, we will not see it again.
That is, we can take the path ``alice -> bob -> kim -> teresa``, or the
path ``alice -> teresa``, or the path ``alice -> bob -> clara``, and in
all of them, each package only appears once.

But if ``clara`` was to depend on ``alice`` this would change:

.. code-block:: text

   alice <----------------------------,
     |                                |
     |                                |
     `---+------------,               |
         |            |               |
         V            V               |
        bob         teresa <-----,    |
         |                       |    |
         |                       |    |
         `---+--------,          |    |
             |        |          |    |
             V        V          |    |
           clara     kim         |    |
             |        |          |    |
             |        |          |    |
             |        `----------'    |
             |                        |
             `------------------------'

Now our previous ``alice -> bob -> clara`` path becomes
``alice -> bob -> clara -> alice -> bob -> clara -> alice -> ...``.
So ``alice`` is granting powers to ``bob``, and ``bob`` is granting
powers to ``clara``, but how would ``clara`` then be the one to grant
powers to ``alice``? ``clara`` cannot just materialise capabilities out
of thin air if ``alice`` has more requirements, so it's not possible
for these arrangements to be resolved by Crochet.

