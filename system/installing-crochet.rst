Installing Crochet
==================

Before you can use Crochet you'll need to install it. The
process is currently not as simple as it should be. So this
page will walk you through all of the things you need to do
to start using Crochet.

Installing Crochet will require using the Terminal
(PowerShell or CMD on Windows), and getting more
familiarised with it.


Install Node.js
---------------

In order to run the Crochet system, you'll first need to `install
Node.js <https://nodejs.org/en/>`_. The website has installers
for both Windows and Mac OS/X, so you can install it by
downloading the installer and running it.

You have the choice of downloading the "Long Term Support (LTS)"
version or the latest version. Both works with Crochet, but the
LTS version is recommended for most users, as it's more stable,
and supported for a longer time.


Linux
'''''

If you're running a Linux system, the official supported way of
installing it is to `download one of the binaries from the
Node.js website <https://nodejs.org/en/download/>`_. And then
setup it manually.


Install Crochet from npm
------------------------

The recommended way to install Crochet is through npm.
Once you have Node.js installed, you can install Crochet from
the terminal:

.. code-block:: shell

   npm install -g @origamitower/crochet

With this you should have a ``crochet`` application available
in the terminal. You can test if everything is okay by running
Crochet in the terminal:

.. code-block:: shell

   crochet

And it should give you something like the following:

.. code-block:: text

   Unknown command (no command provided)
   
   crochet --- a safe programming language
   
   Usage:
     crochet run <crochet.json> [options] [-- <app-args...>]
     crochet run-web <crochet.json> [options]
     crochet package <crochet.json> [options]
     crochet repl <crochet.json> [options]
     crochet test <crochet.json> [options]
     crochet build <crochet.json> [options]
     crochet show-ir <file.crochet> [options]
     crochet show-ast <file.crochet> [options]
     crochet new <name> [options]
     crochet help [<command>]
     crochet version
   
   Options:
     --verbose      Outputs debugging information
