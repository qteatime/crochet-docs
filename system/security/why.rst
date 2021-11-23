Why use capabilities?
=====================

A friend of yours, Kim, is working on a new, cute video game. You've met them
through Clara, who's been a friend for years. And you're glad she introduced
you two, because their games are exactly your jam. So, of course, you're
excited when Kim messages you asking if you'd like to play an early
release of the game and share your thoughts on it.

You download the application that Kim shares with you and have a blast
playing through it. Even though some parts of it are a bit choppy---which
is expected from an early release. You share some of the issues you found
with Kim and tell them how much you're looking forward to the final release.

A few days later, you bump into Clara during your morning walk. But she
immediately follows her greeting with "Hey, just the other day I got
a weird message from you with a suspicious link in it. 'Sup with that?"

You wonder if your computer had been hacked. You change your passwords and
review your security just in case. But then another friend tells you the
same thing. And another. And another. Coincidentally, this all started after
you've played Kim's game. So you bring that up with them.

Upon hearing about it Kim is concerned and apologises, telling you they're
going to double check if anything has gone awry on their end. A short time
later Kim messages you saying that one of the packages they used for the game
had been compromised---had malware inserted into it, which installs itself
to run in the background and send malware to your contacts.

Sadly, for you, the only way you find to reliably get rid of it is to
reinstall your operating system and all of your applications from scratch.
Made slightly less bad because you *do* keep backups of your important
files online---but the annoyance of having to configure everything again
is still there.


What went wrong?
----------------

It's hard to understand the impact of running a program, especially
outside of a phone or a web browser. The problem is that you're not
really just running a video game, or a spreadsheet application, or
a text editor; rather, you're giving full, unsupervised control over
your computer to the application you're running. It's like letting someone
you don't know sit at your computer and use it while you go outside
to buy some snacks. Anything you *can* do in your computer, so can the
applications you run.

Things are a bit less grim in most mobile phones today. Instead of
giving applications free-reign over your mobile device, phone
applications are isolated from each other, and they can do the
things you allow them to do. In order for a phone application to
use your camera, you have to allow it to do so. And the same goes
for using your microphone, photos, files, etc.

This idea of having users decide what applications can and cannot
do is called Capability Security, and its main purpose is to limit
the impact of problems if they do arise. The security model most
computers use, however, is called Ambient Authority---applications
can do anything the user can, which leads to things like separating
regular users and administrator user accounts to try reducing the
impact of problems.

If Capability Security was used in this scenario it could have
caught the issue. Or at least reduced its impact.

For example, let's imagine that the problem started because of a malicious
user publishing a new version of a popular package for 2d graphics.
This new version is able to abuse a bug in the messaging app
to send messages. And for good measure, it tries to keep itself
running in the background.

This new version comes with a watercolour shader, which Kim really
wanted to use for their game's art style. So they immediately download
it and put it in their game. But, if the programming system that Kim
uses had Capability Security, Kim would be greeted with a message
saying that the package now needs to be able to "install applications",
"access and modify all files in the computer", and "send and download data
through the internet". These should raise some suspicion; it's very
unlikely that a graphics package would legitimately have any need for
doing these things.

The message could have helped Kim notice the problem earlier, which
could then be investigated more carefully, and perhaps raised with
the maintainers of the package. But there's a possibility Kim wouldn't
look at these messages and just accept adding the package without reading
what it can do. Or Kim could just be part of the whole thing.

Either way, the packaged game now makes its way to you. You try to run
the game, but since the system uses Capability Security, you're
immediately greeted with a warning screen saying that this game will
be able to "install applications", "access and modify all files in your
computer", and "send and download data through the internet".
Maybe you don't trust Kim *that* much. Maybe this is where you'd stop
and ask Kim what's up with those permission requests.

Of course, there's still a chance that you would just as well ignore
any warning messages and choose to run the game anyway. But the
point here is that Capability Security gives us a tool for negotiating
consent between applications and their users. Allowing applications to
do only that which we're comfortable with them doing, and nothing more
than that. With Ambient Authority we don't have this power---in fact,
we might not even had realised that these things were happening.


The capability approach
-----------------------

Capability Security is a different way of approaching computer security.
One where computers (and applications) are only allowed to do what we
explicitly allow them to do---and nothing more than that. Compared to
security systems based on having different users with different sets
of permissions, a capability system makes consent more explicit---
because the consent that matters here is between us and each individual
application.

We achieve this way of doing security by demanding that applications
request permissions for the things they want to do. If we agree to
grant these permissions, we give the application back a set of "capabilities".
A set of powers to do those things they requested.

Crochet is a programming system based on this idea of capabilities.
But Crochet's boundaries for these capabilities are packages, rather
than complete applications. This allows components within the same
application to also negotiate this consent between themselves. In our
example above, you had to deal with Kim's whole game. But Kim's game
was made out of several little pieces made by different people, and
capabilities would give Kim a way of keeping themselves, and the players
of their game, safe.


