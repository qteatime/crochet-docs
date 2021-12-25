=======================
Contributing to Crochet
=======================

Hi~☆!

Thanks for the interest in contributing to Crochet! Your help is much
appreciated, and this guide will give you some pointers on what you can
do to make things go as smoothly as possible.

Don't worry about making mistakes, though! There aren't hard rules, and
we're here to help you on anything you need :)

First of all...

.. important:: 

   Crochet aims to be a friendly, welcoming, and inclusive community,
   so we do have a few social rules in place to ensure that. In short:
   **be respectful**, but you can see the full details of expectations
   and enforcement on the :doc:`Code of Conduct <code-of-conduct>` page.


How can I contribute?
=====================

Being a user
------------

Crochet is still experimental, the best way you can contribute to it
right now is simply to use it (but don't use it for anything
serious yet).

As an user of an experimental project you'll likely hit many issues,
here's some which you should strongly consider reporting:

:doc:`"Crochet is frustrating to use!" <bug-report>`
    The experience of using Crochet is a large part of its vision.
    Using Crochet should *feel* pleasant and effortless. If you're
    hitting cases where it's unclear how something should be done,
    or it takes too many steps, or it doesn't seem possible at all,
    that's probably a bug. Consider opening an issue for that.

:doc:`"I found a bug in Crochet!" <bug-report>`
    If you've encountered a case where Crochet does not work as
    documented, or crashes, consider opening an issue for that.

:doc:`"The documentation is confusing!" <bug-report>`
    If you can't find something in the documentation, or if the
    documentation's text is hard to follow, that's definitely 
    a bug. Please consider opening an issue for that.

:doc:`"I think Crochet should do this!" <feature-request>`
    Using something will likely inspire you to think "wouldn't it
    be nice if this did That thing?". Crochet is no exception here,
    so there is a design process where you can propose these ideas,
    and we can look into it together from different aspects to see
    how to best make this idea a reality---we want to keep Crochet
    nice to use and safe for everyone.

:doc:`"I think found a security issue in Crochet!" <security-report>`
    This also applies to cases where you simply *feel* unsafe when
    using Crochet. Security issues follow a slightly different
    process to ensure that they can be resolved while causing
    the least amount of harm to existing users. The document
    above goes into detail over this process.


Contributing code
-----------------

If you'd like to jump into coding and submit patches, the following
contributions are currently accepted:

:doc:`Bug fixes <pull-request>`
    You can submit small patches that fix an existing problem in Crochet.
    Keep in mind that, while Crochet is in its experimental release, the
    `known issues <https://github.com/qteatime/crochet/issues>`_ list
    will contain items that we're not accepting contributions for *yet*.
    Items that are accepting contribution will be marked with the
    ``help welcome`` label.

:doc:`Test improvements <pull-request>`
    Patches that fix existing test cases or add missing ones.

.. important::

   Note that no major contributions will be accepted to the VM, runtime,
   and tools, as they will be rewritten before the stable release.


Improving the community
-----------------------

Communities are just as important to a project as its technical aspects.
Besides talking about Crochet, here are some other ways you can contribute
that are more community-oriented:

:doc:`Documentation improvements <pull-request>`
    Patches that improve the phrasing or flow of a particular piece of
    documentation, fix typos, clarify things, or add missing documentation.
    If something confuses you, it probably confuses someone else, too :)


The contribution process
========================

The contribution process differs a bit depending on each type of
contribution, but they all take place on GitHub.
So, in order to contribute, you will have to
`create a GitHub account <https://github.com/>`_ (if you haven't yet).


Do I own my contribution?
=========================

Yes. But you also agree to share your contribution under the same terms
in which Crochet is licensed, the
`MIT licence <https://github.com/qteatime/crochet/blob/main/LICENSE>`_.
See the `GitHub terms of service <https://docs.github.com/en/github/site-policy/github-terms-of-service#6-contributions-under-repository-license>`_ for details.
This ensures that all Crochet users can use your work in their projects :)

.. toctree::
   :hidden:

   code-of-conduct
   bug-report
   security-report
   feature-request
   pull-request
   