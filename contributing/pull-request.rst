Contributing code
=================

If you'd like to send a pull-request to Crochet, you're mostly welcome
(with some caveats).

Generally it's alright to submit patches for issues marked as ``help welcome``.
It's good to raise in the ticket that you plan to work on it just for
coordination, but for small-enough patches it might be alright to just
go ahead and propose the change.

For bigger patches, please discuss in the issue tracker first. These will
generally involve design concerns as well, and there needs to be some
close coordination there.

For new features, regardless of size (even if it looks trivial to you!),
please go through the :doc:`Feature Request Process <feature-request>`
first. Even seemingly harmless additions carry a maintainership burden,
and might have unforeseen security implications.


Setting up the development environment
--------------------------------------

Crochet uses `Git <https://git-scm.com/>`_ and
`Node.js <https://nodejs.org/en/>`_ for the main code base.

The documentation is written in
`Sphinx <https://www.sphinx-doc.org/en/master/index.html>`_. You'll also
need to install Python to work with it.

The website is written in `Jekyll <https://jekyllrb.com/>`_. You'll need
to install both Ruby and Bundlr to work with it.


The runtime
'''''''''''

Create a fork of https://github.com/qteatime/crochet to your GitHub account.
This will allow you to push to it. Make sure you pull the ``main`` branch,
and then create a new branch based on it.

Once you have a repository, navigate to its folder in the terminal and run:

.. code-block:: shell

   $ npm install
   $ node make build

The documentation
'''''''''''''''''

Create a fork of https://github.com/qteatime/crochet-docs to your GitHub
account. This will allow you to push to it. Make sure you pull the ``main``
branch, and then create a new branch based on it.

Once you have a repository, navigate to its folder in the terminal and run:

.. code-block:: shell

   $ make html

You can, then, start a server on the HTML folder to look at the documentation
output:

.. code-block:: shell

   $ cd _build/html
   $ python3 -m http.server

This will start a server on port 8000 if you have Python 3 installed.

The website
'''''''''''

Create a fork of https://github.com/qteatime/crochet-website to your GitHub
account. This will allow you to push to it. Make sure you pull the ``main``
branch, and then create a new branch based on it.

Once you have a repository, navigate to its folder in the terminal and run:

.. code-block:: shell

   $ bundle install
   $ make run

You can, then, open your browser on http://localhost:4000 to look at it
while you make changes.


Testing changes to the runtime
------------------------------

When working with the runtime you can use the ``node make <task>`` in the
root of the repository to compile and test it. ``node make help`` will give
you all supported actions, but you'll likely only use ``node make build``
to compile things and ``node make test`` to run tests (the test task also
compiles the project first).

You can run your own repository's version of Crochet with ``node crochet ...``.
This can be useful if you want to run tests for a library or open a REPL.