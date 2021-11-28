Why are commands ...?
=====================

We've looked into what commands are and how they work in details, but
*why* are things the way they are? Why make commands have all of this
complicated "dispatch" business? Why make them global if everything
else in the language isn't? In this section we discuss some of the design
reasoning behind these decisions.


Why do we need this "dispatch" thing?
-------------------------------------

Most programming languages have functions, and each function has
a name that uniquely identifies it. Mainstream languages have even been
moving towards this direction recently, so Crochet's idea of
dispatch feels like a complication that goes against the current
trends.

Now, it's important to keep in mind here that Crochet's idea of
dispatch *is* complicated. There's a lot to learn and keep in mind
here in order to understand what's happening with commands. In
a language that is security oriented *and* aimed at people who
are not professional software engineers, there must be a very
good reason to pursue something like this. And this reason must
both offset its complexity and guarantee that this won't create
a significant amount of security issues.

For Crochet, there are two primary justifications for this. The
first one is that most of the security mechanisms in Crochet
actually rely on this idea of dispatch. The second one is that
Crochet subscribes (and encourages) a philosophy that software
is written collaboratively.


Dispatch and security
'''''''''''''''''''''

Crochet relies on a form of Object-Capability Security, but in a way
that's slightly different from other systems in this space. Crochet
dubs this variation "type capabilities" because of that.

So, in Crochet, what someone can or can't do is defined by types. In
order to control how much authority a piece of code has---how much you
trust it, and what you're okay with it doing---you control which types
that piece of code has access to.

You reason about security in terms of types. And you control security
in terms of types---by carefully considering which types you let
people access and which you are not comfortable letting them access.
But are these types used to *enforce* this idea of security we can
reason about? That's where commands come in.

Commands are the primary way in Crochet of letting a piece of code
*do* something. Everything else is really just a form of "configuration".
It tells us what the system is. It tells us how it's structured. How we
can think about the different pieces. But we can't *run* them. They don't
really describe any idea of a program behaviour. We need commands to do
things.

Dispatch, then, lets us *restrict* access to these commands based on
how we've restricted access to types---with a bit more of flexibility.
If a command has a requirement on type ``A``, and a piece of code has
no way of constructing one, then it has no way of ever using that
command. ``file-system file: SomePath`` can't be executed if you
have no way of providing an instance of ``file-system``.

If we did not have dispatch, we'd have to figure out how to restrict
access to both types **and** commands, and that would require more
effort to make things secure, which is a dangerous thing to do. Security
should be the default, and require little to no effort, if it is to be
adopted extensively by everyone.

We discuss this in more details in the Security and Capabilities chapter.


Dispatch and collaboration
''''''''''''''''''''''''''

Crochet also assumes that most (if not all) software is created
collaboratively, but this collaboration is more often than not
entirely uncoordinated.

Say Alissa creates a package for rectangles. Later, Max wants to
write a package to handle collisions between objects in a game and
uses Alissa's rectangle package for bounding boxes. Here, Alissa and
Max are collaborating to create a piece of software, but neither of
them might be aware of what the other is doing!

So, what happens if Max loves everything about Alissa's rectangles
package. But later in the development of their collision library,
Max notices that a "does this rectangle contain this point" function
would also be useful. In most languages, Max would either:

1. Have to hope Alissa designed with this extension idea in mind---through
   subclassing or traits;

2. Use some local function for this, which will likely read very differently
   from how rectangles and points are used everywhere else; or

3. Copy Alissa's source code and change the package itself.

Modern languages go for the first one, but that's problematic in
Crochet's case because it requires anyone who's writing a library
to design for extension---and also to predict all cases where
extensions might make sense. This is not a realistic assumption to
make when your target audience is people who are not professional
programmers.

The second one is practical, but the inconsistency makes it
cumbersome, and it's hard to reason about security properties
in this case.

The third one has a particular problem that is seldomly discussed:
it muddies the boundaries of who owns which part of the code. Alissa
wrote it originally, but Max took over it to shape it into their own
thing. How does Crochet users figure out who they're trusting? Can
they simply trust Max, even though Max did not write---and might not
have audited---all of the code?

We discuss all of these security implications in details in the
Security and Capabilities chapter. But the important point here
is that Crochet's choice of dispatch allows Max to write the
function they need, even if Alissa never thought about it,
and still keep it both consistent with the rest of the code,
and consistent with the existing trust boundaries.


Why are commands global?
------------------------

Commands in Crochet are always global, unlike other entities in the
language which are qualified by the name of the package defining them.
This might feel particularly surprising if you're familiar with other
programming languages---there's a trend to make entities be the exact
opposite, and run as far from global concepts as possible.

There are two reasons behind this: consistency and coherence. And
the drawbacks of doing so are attenuated by the idea of dispatch---which
effectively makes commands "less global" by requiring types to access them.


How are global commands consistent?
'''''''''''''''''''''''''''''''''''

Commands can be defined anywhere. Making them always be global means that,
regardless of where we define them, the way we use a command will always
be the same.

This is a big deal for collaborative programming. We want to make sure that,
if we need to extend things, or if we need to move things around, we don't
have to change the code to accomodate that. This consistency in definition
and use helps us achieve that.

There are some particularly nuanced implications here for security. On one
hand, this consistency makes it a bit more difficult to reason about provenance---
what exactly am I trusting when I use a command? But it also is required for
some more advanced security mechanisms in Crochet, such as dynamic capabilities.
We discuss this in details in the Security and Capabilities chapter.


How are global commands coherent?
'''''''''''''''''''''''''''''''''

Let's say Taís wrote a small library for interpolating colours when doing
animations. However, Maki also wrote a library to do that. They're
essentially the same command name, but in two different packages.

If commands were not global, we could have pieces of the code referring to
Taís' implementation of animations, and pieces of the code referring to
Maki's implementation. This can be tricky to catch for developers, but
particularly confusing for users---imagine having a computer program that
sometimes behaves in a particular way, but sometimes behaves in a completely
different way.

Coherence means that commands in Crochet must have at most one behaviour
at any point in time. Making commands global is essential to support this---
if we had them be local them we wouldn't be able to enforce this property
throughout the entire program.

On the other hand, the down side of making things always coherent is that
we would be unable to have both Taís and Maki's command in the same system.
We'd have to pick one or the other to use everywhere. Crochet deems this
acceptable as it leads to less confusing behaviours in the long run.
