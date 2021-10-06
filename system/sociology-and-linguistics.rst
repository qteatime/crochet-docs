Annex B: Sociology and linguistics
==================================

Etymology of Crochet
--------------------

Crochet (/kʁɔ.ʃɛ/ --- `Audio pronunciation on Wiktionary <https://en.wiktionary.org/wiki/crochet#French>`_)
is the English term for needlework with a yarn thread and hooked needle.
It comes from the French "crochet" which also means "hook", and ultimately
derives from Old Norse's "krókr" (hook) --- still alive in Swedish as "krok".

It might sound weird to choose such a name for a programming language,
more so for one designed for security. But it's a name chosen entirely
for its aural aesthetics, not for its meaning. However, meaning can be
derived post-fact. Crochet does try to help weave software by joining
many small components together---though not necessarily made by the
same person.


.. _lexical-restriction-names:

Lexical restrictions of names
-----------------------------

An :term:`identifier` is what Crochet calls the names used for
:ref:`types <type-declaration>` and :ref:`fields <typed-fields>`.
Identifiers can start with a lowercase latin letter
(``a`` to ``z``), and can be followed by any lowercase latin letter
(``a`` to ``z``), a plain hyphen (``-``), or digits (``0`` to ``9``).

A :term:`name` is what Crochet calls the names used for variables.
They're similar to identifiers, but must start with an uppercase latin letter
(``A`` to ``Z``).

Both names and identifiers are case-sensitive. That is, the identifier
``aBc`` and the identifier ``abc`` refer to distinct entities, despite
being comprised of the same logical sequence of letters.

This is very biased towards indo-european languages (particularly English),
but these restrictions exist for two primary reasons:

Syntactical ambiguity
'''''''''''''''''''''

Crochet has a textual representation, and is often written as a plain
piece of text in a text editor. Restricting what can be understood as a
name makes the task of making a computer understand the program unambiguous.

For example, consider a field name such as ``angle in radians``. There's
nothing wrong with this as a field name. Indeed, it can match perfectly what
the programmer has in mind for it. And even declaring this field wouldn't
be as much of an issue: ``type data(angle in radians is integer);``
is perfectly unambiguous.
   
Sadly, this is not always the case. Consider projecting this field:
``simulate for Data.angle in radians until quiescence``. Should Crochet
try to read this as ``simulate for (Data.angle in radians) until quiescence``,
and thus have the simulation run for the value in the ``angle in radians``
field, or should Crochet try to read it as
``simulate for (Data.angle) in radians until quiescence``, thus running the
simulation for the field ``angle`` in the simulation context ``radians``?

Although syntactical ambiguity can be addressed by requiring people to be
more explicit when ambiguity arises (just like bracket use in common
mathematical notations), the experience of making mistakes becomes
rather poor. Because Crochet cannot really infer what is and what isn't
a mistake without broader context (in the above example, both interpretations
make complete sense locally), it's hard for the programming tools supporting
Crochet to help programmers when they *do* make mistakes. What kind of error
message should be displayed? How do we figure out that this is an error?
What can we even suggest to the programmer? Not having to ask those questions
makes the programmer life easier in the long run, at the cost of ruling out
some perfectly reasonable spellings.


Spelling display ambiguity
''''''''''''''''''''''''''

The second problem is a bit more nuanced. Although the restrictions could be
relaxed by allowing any :term:`unicode` letter in the names, thus making the
choice of identifiers less English-centric (and indo-european-centric), doing
so creates a different kind of ambiguity: that of symbolic representation.

For example, consider a program that defines the following types::

    type かめ; // kame (turtle)
    type カメ; // kame (turtle)
    type 亀;   // kame (turtle)

All of these types are different spellings of the same concept, with the
same pronunciation: a turtle (or "kame"). So when a coworker ask you to
instantiate the turtle, how do you figure out which spelling to use? How
should tools like auto-completion handle these identifiers? They certainly
would need to be very language aware to know that they *may* even be
pronounced in different ways. I don't know enough Japanese to design
such system (and all of the other languages I speak are either in
the Latin or Germanic families).

The other problem with allowing a richer set of symbols is in how these
different symbols can be misused and reinterpreted across different
cultures. For example, the ``ː`` (Modifier Letter Triangular Colon, unicode
02D0) is often used in the `International Phonetic Alphabet <https://en.wikipedia.org/wiki/International_Phonetic_Alphabet>`_
to describe that the preceding vowel is a long one. But it looks a lot like
the regular ``:`` (Colon, unicode 003A). A name like ``foldːright:from:``
would be a perfectly valid command name, if all letters were allowed,
but it takes 2 arguments, not 3. ``foldːright:`` is one :term:`keyword`,
even if it may not be readily recognisable as one depending on the
display font users choose or their knowledge of the International
Phonetic Alphabet.

Now, while these edge cases may not be a problem in actual code---and
people should have the poetic freedom to treat their code writing as
an art form in any case---, spelling ambiguity does raise some security
concerns due to how Crochet works.

In Crochet, security is guaranteed based on controlling which pieces of
code have access to what. This depends directly on programmers being able
to recognise names and decide how much trust they want to place on each
component. Crochet then helps with this by making each name unique,
readily identifiable, and associated with a specific source of trust
(i.e.: you should be able to know who you're trusting). Allowing spelling
ambiguity makes this complicated. For example, if a programmer is trying
to invoke a function and auto-completion suggests possible candidates that
match the name, attackers might be able to exploit this to escalate their
privileges by crafting commands with similar names, but different spellings,
and then deceiving users into choosing the attacker version for auto-completion.
Crochet cannot rule out these implementations from the candidate list because
it can only compare exact matches of a name.

Still, this is another example of things that need to be investigated in
the future---particularly due to Crochet's over-reliance on tooling---, as
they will happen to a lesser extent even without spelling ambiguity anyway.



