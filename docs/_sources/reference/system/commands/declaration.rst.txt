What are commands?
==================

A command is a way of describing our program's behaviour. There are other
things that affect how a program works, but commands are the primary one.
Crochet's commands are a bit similar to "functions", "procedures", "routines",
and "methods" in other programming languages, but they have a few unique
things about them.

For example, consider the following command declarations::

    command true and true = true;
    command boolean and boolean = false;

This piece of code defines two commands, but both of them have the same
name: ``_ and _``. The underscores in the name indicate where arguments
to this command would go. In the definition, these underscores indicate
the places where the *requirements* for executing the command go.

So, for the first command, we can execute it whenever both of the arguments
are an instance of the type ``true``. For the second one, we can execute
the command whenever both of the arguments are an instance of ``boolean``.
Remember that types in Crochet create an hierarchy, so the boolean hierarchy
looks like this:

.. code-block:: text

   + any
   |
    `--+ boolean
       |
       |--o true
       `--o false

At the root of this hierarchy we have the type ``any``. Then we have ``boolean``
descending from it. And both ``true`` and ``false`` descending from ``boolean``.
When we use a command, Crochet will pick the one whose requirements are most
closely matched to the arguments.

For example, let's say we have the following use of a command::

    true and true

Crochet will find all of the commands that have been declared with the name
``_ and _`` and then pick one to execute. First, we need to match all 
requirements. In this case both commands we've declared fulfill all of
the requirements: the value ``true`` is both an instance of the type ``true``,
and transitively, an instance of the type ``boolean`` (and ``any``!).

Then, since we have more than one candidate, Crochet needs to somehow
disambiguate this. And the way it does so is by picking the closest matching
one. That is, if we have to walk up the hierarchy up to ``any``, the closest
matching is the one we have to take the least amount of steps. Here, the
command ``true and true`` requires no steps on both sides, whereas the command
``boolean and boolean`` requires one step on each side. Thus, Crochet picks
``true and true``, yielding the result ``true``.

On the other hand, if we had the expression ``true and false``, or
``false and true``. Or even ``false and false``, the requirements for the
``true and true`` command wouldn't be matched, and we'd end up executing
the ``boolean and boolean`` command, yielding the result ``false``.

So, to answer the opening question: a Crochet command is like a function,
it has a name and we can execute that function to do something. But multiple
commands can share the same name, and when we execute one, Crochet will pick
up the closest one that matches all requirements. Some languages call this
a Multi-method.


Commands are global
-------------------

In Crochet, commands are always global. This might come as a surprise since
almost everything else in Crochet is qualified by the package they're in.
So if you define a type like ``player``, what you're really defining is
the type ``some-package/player``. But this is not the case with commands.

If you define a command ``_ and _``, its name will always be just ``_ and _``,
regardless of which package it's defined in.


Signatures
----------

Because commands can have the same *name*, Crochet needs a different way
to refer to specific commands. To do this it has a concept called a Signature.
A Signature combines the name of a command with the requirements to 
execute the command.

Signatures seem simple at the surface, but they're actually a fairly complex
topic, so they're covered in depth in their own section: Signatures and their
uses.


Behaviours
----------

So, if a command describes a "program's behaviour", how exactly does it do
that? Well, if the left side of the command declaration is its signature,
then the right side is its behaviour. Here we use expressions to describe
what the program does if the command is executed.

The distinction between "expression" and "signatures" isn't always very
obvious. A signature may only contain types, and expressions may only
contain values. But because these are two different concepts, they may
(and in a lot of cases do!) look pretty much the same. ``true and true``
can either be a signature (concerning the type ``true``), or an
expression (concerning the value ``true``).

Since the topic is vast, we cover expressions in their own chapter.