Requesting features
===================

You're disappointed that Crochet doesn't do that thing you want it to.
You think that it would be great if it did. You think it would be great
for more users if it did. And so you want to tell us all about your idea.
That's great and very welcome, but we do have a process for this. The
process isn't here to add bureaucracy to everything---it's here to
ensure the feature is aligned with Crochet's vision, and that it won't
cause unintended harm to other users.

This page describes this process.


Pre-requisites
--------------

Crochet feature requests are made in the
`main repository's issue tracker <https://github.com/qteatime/crochet/issues>`_,
on GitHub. In order to send one you'll first need to have a GitHub account.
You can `create a GitHub account <https://github.com/>`_ for free if you don't
have one yet.

You should **make sure that the feature you're requesting aligns with**
:doc:`Crochet's design philosophy <../reference/system/design-philosophy>`.
Some ideas might sound really cool---and may be perfect for other projects!---but
Crochet has certain design principles that guide its features, so there's
a chance your idea might be a poor fit.

You should **be willing to spend a considerable amount of time refining your
proposal and working on identifying the risks and harms** it may have from
different points of view, as well as how to mitigate them. Requesting a
feature **is** a significant investment of time from everyone involved,
not just the people who will be implementing the feature. Making sure that
the design makes sense and is socially reasonable (i.e.: it won't cause
unintended harm when considering different social groups, cultures, and
threat models) is often where a lot of work the work lays.

Your request doesn't need to be perfect on the first try (it's very unlikely
that any request would), but you will be spending time refining it, answering
several questions, and doing your own research on certain issues. Think of it
as a full project that you're undertaking.

And even when you do all of the work, there is still a chance that your
request may be rejected, if the maintainers consider that the risk is too
high for its benefits.


Things that are nice to do
--------------------------

Before requesting a feature, consider searching in the issue tracker to see
if someone has had the same idea before. If you do find something that
looks like your idea, try commenting in that ticket with the things going
through your mind instead.

If you're not sure if what you're thinking of really matches what other
people are, send your feature request *anyway*. It's better to potentially cause
some noise than to let these remain unknown. We can always redirect you
to another ticket if that makes sense.


How to request a feature
------------------------

A feature request is a collaborative conversation to get an idea you have
to fit in the Crochet's design philosophy. The important things in this
conversation are explaining what you expect the feature to achieve, and
why it's great for Crochet to be able to do that. The **required** parts
of this conversation are making sure any potential harms for the feature
are properly mitigated---adding new things is always risky, but Crochet
has a process to manage these risks.

Here's an example of a feature request that is helpful:

    Whenever I'm writing Crochet code, there are cases where I want to
    understand better what's happening to the program. But the debugging
    library currently only supports writing a piece of text to the
    transcript.

    This means that, when I'm working on some model, I need to give my
    types some kind of command to turn them into a textual representation
    to look at them::

        type point2d(global x is integer, global y is integer);

        command point2d to-text =
          "point2d([self x to-text], [self y to-text])";

    This is not that bad when I'm dealing with one or two types. I can
    live with the additional work. But when I'm dealing with, say, a
    hundred of types---especially when they come from something like a
    parsing grammar---, that becomes just too much.

    And there's the issue that complex nesting of these types requires
    a lot of work to convert them to text, and often don't look readable.
    You also can't inspect them interactively once you turn them into
    text, which is a related problem.

    What I would like to be able to do is to just describe the type and
    get this representation for free. So if I have::

        type point2d(global x is integer, global y is integer);

    I should be able to do::

        transcript inspect: [new point2d(10, 20), new point2d(20, 30)];

    And get a readable (possibly interactive) representation on my
    transcript, with the ``x`` and ``y`` fields available, not just the
    name of the type.

It doesn't address all of the requirements, but it is a good conversation
starter. It includes a clear explanation of what frustrates the user, what
they would like to be able to do, and why they think this would be important.
Emotions and feelings are important in features, and this report has a fair
amount of it---while still keeping the dialogue respectful. Always remember
to keep things respectful.

This also goes for insulting other programming languages or technologies.
Avoid doing that in your feature requests. It *is* against the code
of conduct, and may result in a friendly warning.

Anyway! The maintainer may look at this initial request and reply:

    Hey, thanks for the report. I whole-heartedly agree! The current
    way that the debugging library works, requiring text to be sent
    to the transcript, is not great. It causes a lot of friction to
    understand what's happening with your types.

    And the problem with the lack of interactive visualisations for
    the textual representation that you mentioned is really spot on.
    Once you go to a text form you just lose so much to be able to
    do more useful things with the transcript. Ideally we would like
    the transcript to work fully on structured data (we're not there yet
    as you can see).

    Now, as a bit of background. The reason we went with transcript
    only accepting text was that there is no way of expressing more
    granular intentions about when fields should and shouldn't be
    visible, and to whom. So the only reasonable thing to do, even
    when using ``transcript inspect: _`` was to not disclose anything.

    But now that ``global`` annotations have been added, we could probably
    have that mean the same as "public"---they effectively are anyway. And
    we could show those fields by default.

    The other problem is that I don't think this really *solves* the whole
    issue. We could just show the (public) internal structure of a value
    in the transcript (that's what a lot of Reflection-heavy languages do
    anyway), but many types simply make no immediate sense from their 
    internal structure alone (e.g.: consider timestamps), and some types
    are just wrapping boxed values which Crochet can't really disclose
    (e.g.: ``crochet.time/instant``).

    I think we'd need to come up with a way of providing default
    structured visualisations in the transcript which can be overriden
    by user code to provide something that makes more sense to expose.
    And I guess there you run into the other social problem: "what makes
    more sense to expose" is highly context-dependent. So values would
    need to expose multiple "views" somehow.

    How would one even select them, though? That sounds like a long (and
    maybe separate) UX discussion...

Maybe the person who requested the feature is a bit overwhelmed at this point.
Maybe they had not considered all of the implications of the feature. But that's
how things are---if you keep asking questions you'll keep uncovering more things.
Be that as it may, the person replies:

    Oh! I hadn't considered types that really do need a bit of visualisation
    magic to make sense in the transcript. I haven't really run into many of
    them so far, so I can't say that has been weighing on my mind lol

    Maybe we should limit the feature a bit then? First try just making
    the transcript aware of public fields. Figuring out this "views" business
    seems like a lot more of work otherwise, and I'm not sure I'm up to that...

The maintainer replies:

    Sounds good to me! Let's try to keep it limited to making the transcript
    aware of public fields then. I think it works great with using the
    ``global`` modifier as an indication of the user's intent of disclosing
    that value---they're effectively public anyway.

    There are a few problems here though. First is that the VM doesn't really
    track the ``global`` modifier currently, it just uses it to generate the
    command for accessing that field. We would need to modify the VM to keep
    track of it---but you could argue we should've done that from the
    start, ahaha.

    I guess otherwise the idea is that public fields would be recursively
    disclosed, whereas private ones would remain represented in the current
    "secret data" mode? That might actually work without any significant 
    changes to code that *depends* on transcript. You can listen to
    transcript events, but if we just change the display semantics in
    the transcript writer itself then we don't have to worry about code
    that is listening to transcript events and doing their own thing.

    I'll start a design document for this. Let's move the discussion there :)

The maintainer then opens a pull-request targeting the issue with the
following document:

.. code-block:: text

    # [#0032] - Disclose public fields in transcript

    | **Authors** | Q., Max |
    | **Last updated** | 3rd January 2022 |
    | **Status** | Draft |

    ## Summary

    Currently the transcript treats all fields in a type as secret data.
    This means that if you have the following type declaration:

        type point2d(global x is integer, global y is integer);

    And you try to write to the transcript as follows:

        transcript inspect: new point2d(10, 20);

    You'll get the following (unhelpful) output:

        [inspect] (point2d from test-project) [
          x -> (***),
          y -> (***)
        ]

    Since we've introduced the `global` modifier on fields, we can use
    it as an intention of disclosing the field whenever we show somewhere.
    So in this case we'd expect the transcript to include:

        [inspect] (point2d from test-project) [
          x -> 10,
          y -> 20
        ]


    ## Semantics

    TODO


    ## Risks


    ### Leaking secrets

    The primary reason fields are considered secret is due to concerns with 
    data privacy. Transcript events can be listened to by arbitrary code, and
    transcript outputs can be redirected anywhere (e.g.: to files or other
    disk storage). We want to make sure we don't accidentally disclose any
    secret information.

    This is mitigated by restricting the output of this information to
    fields marked as `global`, which are effectively public in any case.


    ### Poor UX

    This proposal is only concerned with allowing `global`-marked fields to
    be represented as public data in the transcript, but any data will be
    shown as-is. And this is not always what one wants.

    For example, if there's a timestamp, we might want to show it as the
    human-readable instant in time it refers to in some calendar. We might
    even want to show it in different ways depending on some context. As
    a result, this proposal does not solve all of the problems uncovered
    by the summary of this document, and they'll need to be handled in a
    follow-up proposal.

    Still, this does improve the current experience slightly for some common
    types, particularly the ones generated from e.g.: Lingua grammars.

The maintainer and the feature requester then continue their discussion by
moving this document forward, talking about the precise semantics and
implementation plans, highlighting more social problems (e.g.: how do users
migrate to this feature once it's released? Does it break any existing code?
Can they be provided with automated upgrade tools to mitigate this breakage?),
etc.

A proposal is considered finished once an implementation for it is merged,
tested, released, and **reaches a stable release**. The last part is important
because features may still evolve (and have their design document changed)
while in their experimental phase. There may always be use cases that were
not considered, or issues that were not foreseen.
