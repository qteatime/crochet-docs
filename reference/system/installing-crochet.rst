Installing Crochet
==================

Before you can use Crochet you'll need to install it. There
are a few ways of installing Crochet, and this page will
walk you through them.

.. 
   (Recommended) Installing the pre-packaged Crochet
   -------------------------------------------------

   This is the recommended way of installing Crochet for anyone
   who isn't comfortable using the command line (or don't even
   know what that might be).

   `Download the zip package for your operating system <https://github.com/qteatime/crochet/releases>`_
   from the Crochet releases page. For example, if you're running
   a Windows machine, you'd install the `crochet-VERSION-win32.zip`,
   where `VERSION` is the version of Crochet you're installing.

   Once you've finished downloading it, unpack the contents of the
   archive somewhere in your computer, and then run the `Crochet`
   (or `Crochet.exe`, or `Crochet.app`) application in the unpacked folder.
   This will open the Crochet IDE (Purr), which contains everything
   you need to build and run Crochet programs.


(Advanced) Installing Crochet with npm
--------------------------------------

You can install the command line version of Crochet using
`npm <https://www.npmjs.com/>`_. For this you'll need to have `Node.js <https://nodejs.org/en/>`_
installed in your computer.

Once you have all of the pre-requisites installed, you can install
Crochet from the terminal:

.. code-block:: shell

   npm install -g @qteatime/crochet@experimental

With this you should have a ``crochet`` application available
in the terminal. You can test if everything is okay by running
Crochet in the terminal:

.. code-block:: shell

   crochet help

And it should give you something like the following:

.. code-block:: text

    crochet --- a safe programming language

    Usage:
      crochet run <crochet.json> [-- <app-args...>]
      crochet run-web <crochet.json> [--port PORT --www-root DIR]
      crochet playground <crochet.json> [--port PORT --target ('node' | 'browser')]
      crochet docs <crochet.json> [--port PORT --target ('node' | 'browser')]
      crochet package <crochet.json> [--package-to OUT_DIR]
      crochet test <crochet.json> [--test-title PATTERN --test-module PATTERN --test-package PATTERN --test-show-ok]
      crochet build <crochet.json>
      crochet show-ir <file.crochet>
      crochet show-ast <file.crochet>
      crochet new <name>
      crochet help [<command>]
      crochet version

    Options:
      --verbose          Outputs debugging information
      --disclose-debug   Treats all types as public data when printing

Run the ``playground`` command to start an HTTP server for an interactive
shell for a specific Crochet package on port 8000.


Editor support
--------------

Besides the built-in Crochet IDE, there is minimal support for
`Visual Studio Code <https://code.visualstudio.com/>`_. The
Crochet extension provides syntax highlighting for Crochet
and related languages.