Reporting issues
================

You've found something in Crochet that doesn't quite work as you expected.
Maybe it's just very frustrating to use. Maybe the documentation around it
is confusing or hard to find. Maybe Crochet just crashes on you whenever
you look at it funny. In any of these cases, you're more than welcome
to report the issue in Crochet's issue tracker.

.. important::

   **DO NOT REPORT SECURITY ISSUES THE WAY DESCRIBED HERE**. Security
   issues have their own special process to ensure that the least amount
   of harm is caused to other users. See the
   :doc:`Reporting security issues <security-report>` page to learn about
   that process instead.


Pre-requisites
--------------

Crochet issues are reported in the
`main repository's issue tracker <https://github.com/qteatime/crochet/issues>`_,
on GitHub. In order to report one you'll first need to have a GitHub account.
You can `create a GitHub account <https://github.com/>`_ for free if you don't
have one yet.


Things that are nice to do
--------------------------

Before reporting your issue, consider searching in the issue tracker to see
if someone has had the same problem before. If you do find something that
looks like your problem, try commenting in that issue with how you're
affected by it instead.

If you're not sure if what you're experiencing really matches what other
people are, report a new issue *anyway*. It's better to potentially cause
some noise than to let issues remain unknown. We can always redirect you
to another issue if that makes sense.


How to report an issue
----------------------

.. important::

   Remember that :doc:`security issues have their own reporting process <security-report>`
   and should **NOT** follow the process below.

When reporting an issue try to be specific about what you **expected**
to happen, and what happened instead. It's good to include information
about what environment you were running as well. For example, programs
may behave differently when ran on Windows or on a Mac. Or even just
in different browsers; Chrome and Firefox have different technologies
under them, and that could be causing issues.

Here's an example of an issue report that is helpful:

    When I try to add days to an instant (I'm using the `crochet.time` package),
    sometimes it will not add the exact amount of days I've specified.

    For example::

        let Date = #plain-date-time year: 2018 month: 2 day: 15;
        Date + 1 day;

    I would expect this to give me `16th February 2018, 00:00`, but instead
    I get `15th February 2018, 23:00`. It looks like it's not adding days,
    but some kind of hours?

    I'm running on this environment:

    - Crochet version 0.13.0 (on the terminal)
    - Windows 11

Here we can see what the user tried, what they expected to happen, and what
they saw happening instead. There's also the versions of the programs that
the user was running that could have some relevance to the issue. That's
a great first step.

From this initial message, since it's related to dates, a maintainer may
ask for additional clarifications. For example, the issue this user was
seeing could be related to Daylight Saving Times. So a maintainer may
reply with:

    Hey, thanks for reporting it! That does indeed look quite odd. It might
    be related to daylight saving times. What timezone is your Windows
    set to?

The user then replies back:

    Oh! That would make sense. My computer is using the Brazilian timezone
    (GMT-03:00).

The maintainer can then try to replicate the issue by changing their
environment to mimic the user's, and with that figure out if their initial
guess was correct. The conversation may continue after that, where both
parties provide additional clarifications until they have a better
understanding of the issue and a way forward to fix it.

In this case, the maintainer might have found that the issue was indeed
related to daylight saving times, and then reply:

    Hey, it seems that adding days to a date really wasn't playing well
    with DST. I've published a new version of the package that should
    fix this particular issue. Can you install ``crochet@0.13.1`` and
    see if it solves the issue on your end as well?

Once everyone is satisfied, the issue can be considered solved, and maybe
added to the next release.


Also useful
-----------

While issue reports are primarily about *having a conversation* about
the problems you're experiencing, sometimes text alone makes this a
bit difficult---because it's hard to get you and the maintainers in
the same page about what exactly is happening.

For issues of programs misbehaving, it's often very useful to provide
a small example, along with clear instructions of how to run it, that
contain the issue you're seeing. This way the maintainers can run and
inspect the example, and better understand all of the things that are
happening in it.