.. _package-configuration:

Package configuration
=====================

.. warning::

   The package configuration side of Crochet is heavily in flux, and the
   ideas described here *will* change soon. This is one reason why this
   page is not written in the same style as the other pages in this
   documentation.


A package in Crochet is described by a folder with a ``crochet.json`` file.
This file describes everything a package contains---essentially, this is a
header for a package image. Storing this image using a file system's nodes
is just an implementation detail---although currently it's the only
implementation too.


The meta-data section
---------------------

A package must contain some meta-data attributes that describe to the
system what the package is, how it can be referenced, and why one should
trust it.

The following root-level fields are part of the meta-data section:

``name`` (string, required)
  An unique name for the package. To reduce synchronisation on this, we
  use the reverse-domain convention popular in Java.

``title`` (string, optional)
  A more friendly name shown to users in the Launcher. ``name`` is used
  if this is not available.

``description`` (string, optional)
  A very short description of what the package does.

``stability`` (string enum, optional)
  An indication of the maturity of the overall package. Can be one of:
  ``"deprecated"``, ``"experimental"``, ``"stable"``, or ``"immutable"``
  (which means only security patches are allowed).

``target`` (string enum, optional)
  The platforms the package is available on. This is currently a very
  restricted idea of target and will change in the future. The possible
  values are ``*`` (all platforms), ``node``, and ``browser``.


The sources section
-------------------

In the sources section, the package needs to describe which pieces of
code are part of the package. Sources can be written in any language
the Crochet system has a compiler for---the VM can only read binary
images in the ``.croc`` format, so the compiler must be able to output
that. Compilers are chosen based on the extension part of the file name.

The current natively supported languages are: ``.crochet`` and ``.lingua``.

Fields in this section (at the root of the file) are:

``sources`` (array of files, required)
  A list of all sources that are to be loaded and executed by the Crochet VM.
  These can be in any language Crochet has a compiler for.

``native_sources`` (array of files, required)
  A list of all sources that are to be loaded natively by the operating
  system in order to provide functionality that Crochet can bind to through
  ``foreign`` clauses. Currently this only supports JavaScript.

  In order to be able to load native sources, the package must receive the
  ``native`` capability from its parent package (or from the user).

Each item in the array is a file. A file is described by the following
type:

.. code-block:: typescript

   type File = string | {
     name: string;
     target: Target;
   }

A file that is not described with a target is unconditionally included
every time the package is loaded. Files with a target can be conditionally
loaded based on the platform it's running and available capabilities.


The dependencies section
------------------------

Packages may depend on other packages. But dependencies form an acyclic
graph due to how capability propagation works, thus if package A depends
on package B, that means package B cannot depend on anything that ultimately
depends on package A.

There's only one field (at the root) in this section:

``dependencies`` (list of dependency, required)
  A list of all packages that this package depends on. Most packages will
  depend at least on ``crochet.core``, since there's not much Crochet can
  do out of the box.

Each dependency has to following type:

.. code-block:: typescript

   type Dependency = string | {
     name: string;
     target: Target;
     capabilities: Capability[]
   }

The string format describes an unconditionally loaded dependency with
no capability propagation---that means that the package will not be able
to do anything *powerful* (only pure computations). The object format allows
controlling when the package is loaded and which capabilities it gets from
the parent package.


The capabilities section
------------------------

The capabilities section describes both the capabilities that the
package defines and the capabilities that it needs in order to work.
There is currently no support for optional or dynamic capabilities,
but that's planned for the future.

The ``capabilities`` field at the root is the only component of this
section, and it allows the following fields:

``provides`` (list of name, required)
  This describes all capability groups that are *exported* from the
  package and available for outsiders to use. The name is simply the
  name of the capability group, unqualified.

``requires`` (list of qualified name, required)
  This describes all capability groups that the package *requires*
  from the parent in order for it to work. This is the fully qualified
  capability group name, e.g.: ``crochet.random/read-shared-instance``.