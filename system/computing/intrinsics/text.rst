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


Text composition
----------------

An interesting aspect of text is that we often want to combine different
pieces, with different grammars and semantics. This is not really a
computing thing; handwritten text in a piece of paper may comprise
different languages, formatting, colours, and so many other aspects.

Likewise, it's quite common for some computer program to include text
that contains parts in another language. For example::

    "The sun was out in full force again; summer has arrived. And
     there's only one way to describe this feeling: 夏バテ."

Here we have a piece of text literal in Crochet that includes text
in both English and Japanese---the Japanese part, "natsubate", or
"suffering from summer heat", is used to capture and emphasise the
leading sentences. These kind of multi-lingual pieces of text are
very common, though more often would comprise pairs like English
and French, or English and Latin.

So Crochet literals supports some of these compositions already---though
in this case that's by plain luck, as there's nothing that tells
Crochet that this *is* a composition. Crochet is not aware of
the intrinsic semantics of these sentences; it does not care about
what they mean.

Now, computers sometimes care about the meaning of these pieces of
text, too. And at that point composition becomes more complicated.

Consider::

    let Room = "The ceiling of the log cabin is in the same wood
                you see in the walls. Nothing fancy, but well
                kept still.";
                 
    let Chandelier = "At the centre there’s a chandelier with
                      three gas lamps.";

Here we have two separate pieces of text, one which describes a room, and
another which describes a chandelier. We might have an interactive fiction
where these pieces of text might be combined depending on certain things
happening in the simulated game world. For example, the number of gas
lamps might change, thus changing the description of the chandelier.

But when we present this to the player we still want to make sure that
they will see the *combined* piece of text; as if it was a single literal
to begin with. We want them to see this:

    The ceiling of the log cabin is in the same wood you see in the walls.
    Nothing fancy, but well kept still. At the centre there’s a chandelier
    with three gas lamps.

In Crochet, this is achieved by using the text composition form---called
interpolation. The composition form is similar to the text literal---but
it allows us to insert different things within the text, by using an
expression within square brackets. For example, we could combine the
example above using::

    "[Room] [Chandelier]"

This just makes it so all of the text in ``Room`` is followed by all
of the text in ``Chandelier``. We could also have written it as such::

    "The ceiling of the log cabin is in the same wood
     you see in the walls. Nothing fancy, but well
     kept still. [Chandelier]"

They both have the same semantics.


Non-text composition
''''''''''''''''''''

Interpolation is not limited to pieces of literal text in Crochet. We
can compose any kind of Crochet value using it. This is often used to
handle things like text formatting. For example, you might want to
present some pieces of text in bold or italic letters. Or you might
want to use a different type face, or a different size, or colour.

In Crochet, these will generally be commands that produce a
Crochet value that represents this "intention" of formatting
the text---or adding non-textual things to it. For example::

    "You inspect the bracelet in your wrist. It [bold: "looks"]
     like an elastic band. The one that is perhaps too comfortable
     to wear, as you hadn't noticed it there sooner."

Here we have ``bold: "looks"`` within square brackets---the double
quotes here are not escaped because, within the brackets, we can
write any expression; Crochet will not get confused as the
brackets provide an explicit beginning and end for it.

What this ``bold: _`` command would do is to create a Crochet
value that can represent its piece of text in bold font. Essentially
giving us something that looks like this:

    You inspect the bracelet in your wrist. It **looks**
    like an elastic band. The one that is perhaps too comfortable
    to wear, as you hadn't noticed it there sooner.

Internally, Crochet just keeps track of which parts of the
interpolation are literal pieces of text, and which parts are
some arbitrary Crochet value. But it's up to the code handling
these interpolations how to associate a meaning to the entire
composition.


Text and trust
--------------

Crochet considers all pieces of literal text to be "trusted"---that
is, they originate from within the code itself, and so the meaning
should be known. At least as long as the package which includes
them is also trusted.

On the other hand, pieces of text that come from outside of the
program---say text that user can type and provide to your program,
or the contents of a file---are always considered "untrusted".
Which means that Crochet cannot verify its origin, and cannot
decide if that piece of text is "safe" or not.

Whenever pieces of untrusted text are combined with pieces of
trusted text, the entire interpolation becomes, itself, untrusted---
but the pieces within this interpolation maintain their original
trust level. This behaviour allows computations that interpret
these interpolations to know which values need to be a bit
more restricted, and subject to a bit more of scrutinity,
when looking at them. Safe composition of values relies on
this property.

To put this in more concrete terms. Imagine that you allow
users to type the name of a file, which your game can then
use as their avatar. These avatars are stored within a particular
folder, so in order to load them you use the following
interpolation::

    let Avatar = "images/avatars/[Filename]";

So when Alissa types in ``cat.png`` as her file name, she'll
get ``images/avatars/cat.png`` as her avatar. Maki, however,
is trying to be a bit clever here. She sees the potential to
*break* our little game. So she types ``../game-logo.png`` as her file
name---and gets ``images/game-logo.png`` as her avatar.

This example doesn't have any particularly bad implications,
but it still lets us see that when we combine pieces of text
naïvely, what we expected is not *always* what happens---and
a lot of security issues happen because of this mismatch
between what we expected to happen and what was actually
*possible* to happen, given the program we wrote.

Crochet aims to keep that mismatch to a minimum, which is why it
goes a bit further with the distinction between trusted
and untrusted values. This is then used by code interpreting
these interpolations to ensure that it's very unlikely that
they will do confusing things---most of the time, you don't
really need to *worry* about it, unless you're the one writing
one of these interpreters.
