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

`Trace debugging (crochet.debug.tracing) </_static/api/crochet.debug.tracing.html>`_
  Provides tools to record and analyse different aspects of the execution of
  Crochet code.

`Mathematics (crochet.mathematics) </_static/api/crochet.mathematics.html>`_
  Extends numeric support with trigonometric functions.

`Concurrency (crochet.concurrency) </_static/api/crochet.concurrency.html>`_
  Provides Crochet's primitives for concurrency: actors, CSP channels, promises,
  discrete streams, and reactive variables.


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

Network
-------

`Network types (crochet.network.types) </_static/api/crochet.network.types.html>`_
  Provides safe types for parsing and manipulating common pieces of
  data found in network-related code, such as URLs.

Wrappers
--------

`Browser API wrappers (crochet.wrapper.browser.web-apis) </_static/api/crochet.wrapper.browser.web-apis.html>`_
  Small wrappers over common browser APIs, with capabilities.

Graphics and User Interfaces
----------------------------

`Agata (crochet.ui.agata) </_static/api/crochet.ui.agata.html>`_
  Library and runtime for Crochet's reactive GUI framework, Agata.
