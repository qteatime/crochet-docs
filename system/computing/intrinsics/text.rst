Textual models
==============

.. warning::

   Text is complex and everything that is written here most likely will
   change.


Text is a big part of most kinds of programs, and it shows up quite
often in interactive fiction as well. Crochet approaches textual
representation in a way that tries to make it safer and more
respecting---and supporting---of different languages and cultures.


Text literals
-------------

Text can be described in Crochet using the text literal form. This
allows one to provide any kind of Unicode piece of text, which is
sufficient to support people to capture text in languages like
English or Japanese, and to use emojis::

    "Hello! こんにちは 😊"

Literals can also contain multiple lines::

    "There’s an unfamiliar scent.
     An unfamiliar feeling.
     You’re laying down on a cold floor---you feel
     the irregular stones beneath you,
     but you haven’t seen them yet.
     Your eyes remain shut."

These forms may still contain double quote (``"``) characters, but
because they both indicate the start and end of the literal, including
them requires the character to be escaped---that is, written with
a preceding backslash: ``\"``::

    "They exchanged some glances. \"Are you not eating...?\" Awra asked."

Alternatively, literals can be started with ``<<`` (double left angle brackets),
and end with ``>>`` (double right angle brackets). In this form, double quotes
don't need to be escaped::

    <<They exchanged some glances. "Are you not eating...?" Awra asked.>>


Unicode escapes
'''''''''''''''

Crochet allows characters to be written using their explicit unicode escape
sequence, rather than its representation. The notation uses ``\u`` followed
by the four hexadecimal unicode digits.

For example, the ASCII exclamation mark (``!``) has the unicode number
``0021``, so the escape sequence would become ``\u0021``. The following
are equivalent::

    <<Hello!>>

    <<Hello\u0021>>

There are certain situations in Crochet where characters must be written
in their unicode escape form.


Handling of white-space
'''''''''''''''''''''''

Any leading or trailing white-space character in a line in a text literal
is ignored by Crochet. That is, the following literals are equivalent::

    <<    Hello!    >>

    <<Hello!>>

As are the following::

    <<First line
          and second line
        and third line       >>

    <<First line
    and second line
    and third line>>

White-space that is not leading or trailing in a line is collapsed. That is,
multiple space characters are treated as if there was a single space character.
Thus, the following are equivalent::

    <<This   has    many     spaces,    but   Crochet    doesn't    care>>

    <<This has many spaces, but Crochet doesn't care>>

All white-space characters are normalised, which means that tabs (unicode
``\u0009``) becomes a single ASCII space (unicode ``\u0020``).

White-space that must be preserved in the literal needs to appear as
its unicode escape code in the source code, but tools are free to provide
friendlier presentations and editing interfaces. For example::

    <<One\u0009Two\u0009Three>>

Is how one would express the words "one", "two", and "three" separated by
tabs.


Handling of invisible characters
''''''''''''''''''''''''''''''''

Unicode supports invisible and control characters---characters that don't
really have any glyph representation, but change how the text is interpreted
by the program presenting it on the screen.

Crochet requires all invisible and control characters to appear as explicit
unicode escape sequences in the source code, but tools are free to provide
friendlier presentations and editing interfaces.


Unicode normalisation
'''''''''''''''''''''

Unicode allows text that can be presented in the same way on screen to be
written in very different forms. For example::

    <<cafe\u0301>>

Is presented in the screen in the same way as::

    <<café>>

But in the source code, these are different pieces of text---they're composed
of different characters. In Crochet, any text written in a literal is
converted to its canonical composed form. That means that in both of these
cases, Crochet will *act* as if the source code contained the second form,
where the ``é`` character is a single character.

Because Crochet uses the canonical form---where it's assumed that the meaning
of both representations will not change---there are some cases where one may
consider the meaning to be the same, but Crochet cannot make that inference.

For example, the following pieces of text could be considered to mean the
same thing in Japanese::

    <<ネコ>>

    <<ﾈｺ>>

    <<ねこ>>

    <<猫>>

All of these pieces of text *can* be read as "neko" (cat), but the choice
of spelling and the way they compose with surrounding pieces of text might
be relevant to their *meaning*, therefore Crochet does not do any
normalisation for these cases automatically.



