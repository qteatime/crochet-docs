===================================
Welcome to Crochet's documentation!
===================================

.. warning::

   These books are still being written and should currently be considered
   unedited drafts. As Crochet itself has not stabilised yet, any concept
   covered here might change in the future---particularly in flux sections
   will be marked with an admonition like this one.

The official documentation is divided into sections and books,
and cover different aspects of the technical and practical sides
of Crochet, as well as providing community and learning
resources.


Introductory books
==================

These project-driven books are the perfect way to start your
journey through Crochet. Pick the one that best suits your
goals and experience with programming, and create away~.

(Work in progress)

..
  .. hlist::
     :columns: 1
  
     * :doc:`Crochet for Functional Programmers`
           For people who're familiar with functional programming.
           This example-based book will guide you through the different
           concepts in Crochet by having you construct a few
           different and fun toy programs.
  
     * :doc:`Simulating with Crochet`
           For people who have never programmed before. This book
           will guide you on your first steps with creating simulation
           and AI-based games.


Reference books
===============

Here you'll find complete treatises on the technical aspects
of Crochet and the tools that it includes. All of these books
assume some previous familiarity with Crochet.

But ever wondered how things *really* work? Ever asked why things
are the way they are? Concerned about whether approaching things
a certain way will be fast enough? You'll find the answer to those
troubling quesitons here.

.. hlist::
   :columns: 1

   * :doc:`The Crochet System <reference/system/index>`
         A reference book on Crochet. Dives deep into the
         technical details, but also the design and
         sociological ones.

   * :doc:`Crochet's API Reference <reference/api/index>`
         Short and cross-referenced API documentation on the
         built-in Crochet packages.

..
   * :doc:`Core: Crochet's IR`
         A book on the mathematic formalism behind Crochet's
         intermediary representation. Aimed at programming language designers
         and compiler developers.


Cookbooks and Cheatsheets
=========================

.. hlist::
   :columns: 1

   * :doc:`The Brief Syntax Cheatsheet <cookbook/brief-syntax/index>`
         A short document describing all syntactical forms in Crochet.
         Assumes that the reader is familiar with the concepts in the
         language.

..
   * :doc:`A Catalogue of Techniques`
         A book of recipes for how to express different programming
         techniques in Crochet.


Contributor guides
==================

.. hlist::
   :columns: 1

   * :doc:`Contributing to Crochet <contributing/index>`
         A short book on how to contribute to Crochet in different
         ways. From ideas to community work and code.



Indices and tables
==================

.. hlist::
   :columns: 1

   * :ref:`Search page <search>`
         Search this documentation.

   * :ref:`General Index <genindex>`
         Quick access to all terms and sections.

   * :doc:`Glossary <glossary>`
         Explains all technical terms that you may encounter
         in the Crochet books.

.. toctree::
   :hidden:

   reference/system/index
   reference/api/index
   cookbook/brief-syntax/index
   contributing/index
   glossary