What's Crochet?
===============

Crochet is a tool for creating and remixing interactive
media: applications, games, interactive books, animations,
and so on. This is generally called a "programming system".

What differentiate Crochet from other programming systems
is that it tries very hard to make the experience of using
it as safe and privacy-respecting as possible. Even if you
download random pieces of code from the internet and include
in your own application. Even if you run a game some stranger
has sent you on social media. Even if you're not very familiar
with computer security. Even if you have absolutely no idea
of what you're doing.

One of the core principles of Crochet is that you should *feel*
safe to experiment with your computer as much as you want,
without having to worry about questions like: "If I install
this application, will it try to steal my files?" or "What if
I try this and it breaks my computer?"

There's nothing particularly *wrong* with wondering about these
questions. But life is a lot better if you don't *need* to worry
about them, because the tool you're using tries to give you a
safe environment for experimentation. Crochet aims to be that
kind of tool.


What is a programming system?
-----------------------------

So I mentioned that Crochet is a "programming system". But what
does that mean, really?

Well, "to program" something means that we create something
that the computer can understand. This is generally going to
be some kind of interactive application, like a game or an
interactive book. But interactivity isn't always necessary or
wanted. We might want to create digital media that has no
user interaction: like mixing a digital comic book with
sounds and some animation. Or even something like a visual
novel with no choices.

Sure, some of these could well be a movie. They could be created
in a video editor program. Crochet just gives you a different
tool to approach this kind of creation, which might or might not
be more interesting for you. That said, this book and other
Crochet materials focus more on *interactive* media, since
that's the point where you usually need to reach out for a
programming tool.

But what does it mean for it to be a "system"?

This one is a bit trickier. I did mention that Crochet is
"a tool". But more accurately, Crochet is really "a set of
tools". Just like office suites come with several different
tools that may complement each other. Crochet is the same.
Each tool has one different purpose in the creation of
interactive media.

This "set of tools" becomes a "system" by making them work
together rather seamlessly. The tools are *meant* to work
together. You might find yourself generating dialogues with
Surface Crochet, then using this dialogue in an interactive
fiction you wrote in Novella, and you test and develop the
game within Purr.

Surface Crochet, Novella, and Purr are some of the tools
you will find in the Crochet system. And anything you
create will likely use many of them. But that doesn't mean
you need to learn everything about these tools in order to
get anything done---indeed, some times you might not even
realise you're using a different tool, because they're all
part of the system. And they all support some specific
creation workflows. And these workflows will most likely
use only part of the tool.

You learn and think in terms of these workflows, rather than
the individual tools themselves. Most of the time.


How is Crochet safe?
--------------------

For most applications you install or run in your computer,
the application is able to do anything that you, yourself,
would be able to do. It can read any file. *Delete* any file.
Download malware from the internet. Or even just upload your
personal files to random places---and you would have no say
in any of this.

Which is why, when you install or run an application, you
must trust that it will do no evil, right? If you just install
applications from well-known companies, from people you trust,
surely you must be on the safe side, right?

Things are not so simple, sadly. Even when applications may
not, themselves, be evil, they may include bugs which allow
outsiders to abuse your computer in the same way. For example,
a bug in something like Chrome's auto-update feature could be
abused to download and install malicious programs from the
internet---as if the malicious program was simply Chrome.

And bugs aren't even the only way malicious programs may end
up in your computer. Even when you only install applications
from trustworthy sources, and these applications go to lengths
to protect against these kinds of bugs, they will still include
components that were created by other people. And these
components will not always follow the same rigorous and safe
development practices as the people you're trusting. There's
a chance that an attacker will target these smaler components,
in the hopes that they can get malicious programs into common
applications unnoticed---this kind of attack is, in fact,
becoming more common nowadays.

As an independent creator, you're likely going to be
relying a lot on parts that were not made by you, or by
the people who made Crochet. The same concerns apply here.
It would be easy for someone to sneak malicious code into
a component that you use, and that malicious code would
then affect both you and the people consuming the things
you make, causing all kinds of havoc.

Because Crochet aims to support a remixing culture---where
creators are encouraged to modify other people's creations---,
this scenario becomes much more common. And so Crochet takes
a different approach than most tools here by being a
"safety first" tool. What this means is that, instead of
just allowing any component to do whatever it wants, they
are only allowed to do what you explicitly decide they can
do.

This is similar to how modern phone OSs work. For example,
when you try to run an application on your phone that requires
access to your photo library, your phone will ask if you want
to grant that access or not. Crochet does a similar thing,
and whenever you use a component made by someone else, you'll
see what that component can do, and get to decide if that
sounds like a reasonable risk.

We discuss all of this in details in the Security chapter.


What can I do with Crochet?
---------------------------

So if Crochet is a tool for creating interactive media, what
exactly does that mean? What can you really make with it?

Crochet was originally designed---and still heavily leans
towards---creating video games. Particularly story-based
ones, with characters that may be controlled by an AI.
So you'll find tools that can help you build interactive
fiction, visual novels, RPGs, and other kind of simulation
games.

But as Crochet evolved, it also became practically usable for
other purposes as well: things like software verification,
automating tasks in a computer, procedural generation
of content (things like a Twitter bot), and even building
tools for programming languages.


What can I not do with Crochet?
-------------------------------

Crochet is what's called a "general purpose programming system".
In theory, this would mean that you can create anything with
it. In practice, things don't really work like that.

Once you step away from the tasks mentioned above you'll find
that it becomes increasingly difficult to get anything done. So,
sure, you could turn the knobs enough in Crochet to make music
with it, but you'd find no tool, documentation, or community
support to do so---you'd be on your own. You'd have to build
most things from the scratch. And that's far more effort than
most are willing to spend.

It's possible that, in the future, Crochet gains more tools
and communities that expand what you can do with reasonable
effort. But for now, you should consider anything outside
of the things mentioned above as outside of the realm of
things you'd do with Crochet.
