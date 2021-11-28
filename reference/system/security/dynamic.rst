Dynamic capabilities
====================

Crochet's push for Types as Capabilities has the primary goal of
making it possible for tools to help people understand the risks
they are taking by running programs in their computer. Their static
nature is what allows that---but this comes with its own problems.


Why do we need them?
--------------------

When everything is static it means that you both need to grant
all of the capabilities ahead of the time, and that you can never
take back the capabilities after you grant them. And that poses
both security and usability issues.

To address this, Crochet also allows capabilities to be dynamically
granted---that is, granted while the program is running, rather than
before running it. This is necessary for contextual capabilities
(a future extension to Crochet's capability system necessary for
usability), and also for giving packages control over temporary,
restricted, and revocable capabilities.

For example, consider the case where we've asked the user to choose
a directory on their computer to save novels that our application
can generate. We then want to allow the package that handles the
novels to read and write to this directory (and *nothing else*),
but only if the user has given us this power---the user might simply
not wish to save the novels, and thus should never be even bothered
with being asked for this power; the user should not be made aware
that this specific Crochet capability exists until the application
needs it.

Static capabilities cannot solve this problem because they would
both make the user aware of the power before running the program,
and would never be aware of which directories could be chosen by
the user---after all, that is something the user decides *while*
running the program, not before running it.


Objects as capabilities
-----------------------

By using Types as capabilities, Crochet allows us to reason about
powers and risks. And then it allows us to control how this power
is distributed in the program configuration---who gets access to
what.

But once the program is configured, what powers are effectively
used is determined by Commands. And these commands are selected
by types in principle---but they don't *receive* types, they
receive objects; the little pieces of information that we get
from Constructing a type.

And this idea of Commands that are selected by Objects is core
to languages that use objects as capabilities. If you can get
your hands on an object, then you've gotten the power to its
commands as well. And because these objects flow through the
program in arguments to commands, or as return values from
various operations, we're no longer restricted to powers
that the configuration dictates; but powers that the execution
of the program chooses to grant.

For example, if we continue with our opening problem in this
chapter---that of a program that lets users save novels to a
directory of their choosing (and nothing else), then we could
have a powerful package that handles asking the user for this
directory::

    command game ask-storage-directory -> directory do
      // Implementation intentionally omitted
    end

The implementation of this command isn't too relevant, but it
returns a ``directory`` object. This ``directory`` object would
then give one powers to read files and save files in that directory
alone---without even being made aware that other files and directories
exist.

We can then pass this object around until it reaches the other
package that generates novels. This package has no powers from its
configuration, but it's able to accept directories and use them::

    command novel save-to: (Directory is directory) do
      let File = Directory create-file: self title;
      File write-text: self contents;
    end

Here we're able to create a file inside of the directory, and write
to that file. But that's all we can do. We can't break out of this
directory and access other files---or modify other files. Indeed,
we can't even be sure that this directory is an *actual* directory
in the computer. It could be a Zip archive. It could be a database.
It could be a storage service that is accessed through the internet.
As long as the expected semantics are the same, the user of this
object cannot know its true form, and it should not care.


Revocable capabilities
''''''''''''''''''''''

A revocable capability is an object capability that can stop working
at the convenience of whoever granted it. For example, if we wished
to grant some piece of code a one-use capability for saving data,
we could do so by making an object that exposes commands which only
work once. This could be achieved by using cells::

    type save-once(used is cell<boolean>);

    command #save-once make = new save-once(#cell with-value: false);

    command save-once save: Data
    requires not-used :: not (self.used value)
    do
      // Implementation of saving the data goes here
      self.used <- true;
    end

Here the usage of the command ``_ save: _`` is guarded by the ``not-used``
contract, which makes sure that the ``used`` field is false. When we save
the data, we mark this ``used`` field as true, consequently making the
``_ save: _`` command unusable from there on.