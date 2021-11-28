Annex A: Design philosophy
==========================

Crochet was born to make programming interactive fiction games more
accessible to writers and artists---or rather, more accessible to
non-professional programmers who want to use computers for their
own creative endeavours.

Both Core Crochet and Surface Crochet have evolved a lot since them,
but they still embody much of this philosophy. If the language was
described in a single sentence, it would be: "A tool for safely
experimenting with interactive computer art." For a broader meaning
of "art," that covers any creative uses of computers.


Design principles
-----------------

Core to this goal are three tenets:


"Safety comes first!"
'''''''''''''''''''''

If we want people to experiment and collaborate in programming, we must
provide them with a safe environment to do so. Collaboration isn't optional,
there is no way of building any modern software without relying on other
people's code. And as soon as we accept it, we also need to accept that
the threats to safe experimentation aren't just accidental damage; we must
also protect people from malicious actors.

Crochet goes through great lengths to make experimentation safer: adopting
the Principle of Least Authority, using Capability Security, isolating
effects with Algebraic Effect Handlers (this is important to avoid
accidental damage during experimentation), and controlling resource usage
through Computational Zones.


"Privacy is required for safety!"
'''''''''''''''''''''''''''''''''

Security problems may have immediately visible consequences, but privacy
problems don't always have that. However, both of these can make people 
*feel* unsafe, and both of them have the potential of harming actual
people. Therefore, if we're aiming for a safe experimentation platform,
we must value privacy as much as we value security.

The combination of security and privacy-respecting code requires us to
treat all pieces of code as "untrusted and potentially dangerous". So
Crochet approaches privacy through ideas from Information Flow combined
with ideas from Capability Security. The way it actually addresses
the problem does not provide any non-interference guarantees, but
the guarantees it does provide are often reasonable for the domains
Crochet aims for.


"Rich, immediate feedback is key to experiment"
'''''''''''''''''''''''''''''''''''''''''''''''

When we're experimenting with an idea, we may approach it from different
angles we want to observe what the effects of all of these approaches are,
how they compare to each other. We want to understand, and sometimes this
"understanding" requires comparisons as well.

Programming tools often fall short of addressing this, and instead focus
on static reasoning, requiring people to learn and reproduce all of the
semantics by heart in order to figure out the effects of certain changes.
Meanwhile, data science tends to rely a lot more on observations of data
with things like interactive notebooks.

Live-programming, immediate feedback, and direct manipulation aren't exactly
new concepts in programming language tools, but they are often not well
integrated or flexible. The confinement of most REPL tools to the command
line does them a disservice by limiting too much of the data representation
and interaction---because you want to interact with it, explore specific
cases, figure out patterns in it, understand how they relate to your program.

So Crochet takes a tooling-first approach, preferring features that lend
themselves well to immediate feedback and hot-patching (required for
live-programming), as well as allowing people to choose different
representations for the same piece of data, and different ways of
manipulating it (direct manipulations or programmatic manipulations).
This is one of the reasons Crochet limits things like lambdas, which
are so common in functional languages, and approaches interactive
programming through the idea of Program Versioning.


Language domains
----------------

Although people often categorise languages like Crochet as "general-purpose,"
the category is unhelpful in understanding the language's tradeoffs, usage,
and philosophy. So, instead, Crochet is very explicit with the domains it's
optimised for.


Interactive fiction
'''''''''''''''''''

The original motivation to design a language like Crochet was to make it
easier to build Interactive Fiction games, particularly ones with strongly
independent, AI-driven NPCs. The term "Interactive Fiction" here covers
many narrative-driven (and adjacent) games such as Visual Novels, RPGs, and
Environmental Simulations.

Crochet helps these games with a Symbolic Logic sub-language that relies
on a Global Fact Database. A Simulation sub-language allows expressing
game rules (and game agents' behaviour) declaratively, and in a way that
allows the runtime to verify and optimise their execution.


Software verification
'''''''''''''''''''''

It turns out that Model Checking falls quite closely to the idea of 
expressing game rules in a declarative and verifiable manner. Crochet lends
itself better to Stochastic Model Checking (such as Property-Based Testing),
and Bounded Model Checking, since there are usability features of the
underlying symbolic logic that prevent translations to common model checking
tools.

Crochet's Algebraic Effect Handlers and Tracing Debugger provide a very
good basis for applying model checking to *external* languages, in ways that
are recordable, reproducible, and interactively explorable going both forwards
and backwards in time. The Simulation sub-language allows one to express
these models in concise ways, in similar fashion to tools such as Alloy.


Cross-platform automation
'''''''''''''''''''''''''

Crochet's approach to interactive experimentation, along with the idea of
Algebraic Effect Handlers and Capability Security, provides a safe
way for people to play around with software automation. The
Interactive Playground provides richer feedback than what is possible
with common Shells (such as Bash, Fish, etc), while at the same time
being cross-platform and reproducible (one can turn a playground session
into an actual program).

The playground is particularly nice with potentially destructive operations,
as it offers the possibility of "dry-running" for free, without any changes
to the code, underlying programs, or even online services. Reproducibility
follows the same, with the possibility of recording and replaying sessions
without hitting external services.

The obvious drawbacks here are that common \*nix tools need to be reimplemented
in Crochet, but since this is a domain Crochet aims to excel at, reimplementing
these tools with the mentioned features and reasonable performance is a 
goal for the standard library as well.


Procedural generation
'''''''''''''''''''''

Some games, such as Roguelikes, rely a lot on procedurally generated content,
but this is often useful for Interactive Fiction and simulations as well. The
Simulation sub-language's use of Stochastic Search allows some common
procedural algorithms to be written declaratively in Crochet.

Further, supporting Interactive Fiction with strong AIs also requires work on
things such as procedural dialogues, and these same tools can be used for
non-game procedural content such as Twitter bots.


Language tools
''''''''''''''

Crochet is a "language-driven" system, through the lenses that we interact
with computational concepts through languages; Even "direct manipulation"
forms a language, where the ways in which we can manipulate things is dictated
by a set of composable rules. A system like this, heavily dependent on tooling,
needs ways in which users can extend the system to fit their own context.
This means that Crochet *has* to support user-extensible IDEs, user-extensible
Debuggers, user-extensible REPLs, etc. And these users should be able to modify
any aspect of these tools to fit new languages (interactions, manipulations,
rules, etc).

To this end Crochet is somewhat similar to Language Workbenches, such as
Spoofax, but also similar to other "language-driven" systems, such as
Racket and Glamorous Toolkit.