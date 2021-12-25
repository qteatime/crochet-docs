=======================
Crochet's API Reference
=======================

This is a temporary page that links to reference docs built with
Crochet's ``docs`` command. The following packages are available
in the standard distribution:

Basic packages
--------------

`Core (crochet.core) </_static/api/crochet.core.html>`_
  Provide the most basic types and commands to most programs: text manipulation,
  numeric types, basic collections, error handling, etc.

`Debug (crochet.debug) </_static/api/crochet.debug.html>`_
  Provides a simple transcript (for trace-based/print-based debugging), and
  a simple tool for timing pieces of code.

`Mathematics (crochet.mathematics) </_static/api/crochet.mathematics.html>`_
  Extends numeric support with trigonometric functions.


Language and Parsing
--------------------

`JSON (crochet.language.json) </_static/api/crochet.language.json.html>`_
  Provides support for reading and writing data in the JSON language.

`Lingua (crochet.text.parsing.lingua) </_static/api/crochet.text.parsing.lingua.html>`_
  Provides a runtime for Lingua grammars---the recommended way of parsing
  text in Crochet.

`Regular Expressions (crochet.text.regex) </_static/api/crochet.text.regex.html>`_
  Provides basic support for manipulating text with regular expressions. Do not
  use this for parsing text!


Randomness
----------

`Random (crochet.random) </_static/api/crochet.random.html>`_
  Provides support for predictable random number generation.


Date and time
-------------

`Time (crochet.time) </_static/api/crochet.time.html>`_
  Provides support for talking about time in terms of points in time,
  lengths of time, and calendar-based dates.