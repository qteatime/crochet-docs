Reporting security issues
=========================

You've found something wrong in Crochet, and just realised that it has
the potential to harm others. Maybe there's a way for code to access
files without getting a capability, and then send this data over the
internet. Maybe there's a way of making a trusted piece of code
execute other Crochet code with the wrong set of capabilities. In
any of such cases you should report the issue **privately** to the
security group first. This way we can coordinate on mitigation
procedures to reduce the amount of harm to users.


Please `e-mail the security group <mailto:security@qteati.me>`_
privately to discuss the issue. You should include enough information
in it for the maintainers to understand the issue and its impact.

Even if the issue is related to data privacy, please do not include 
any actual personal information in the email.


Patch coordination
------------------

Once a security report is received, a maintainer should acknowledge
the report within the week. And then discuss when a patch can be made
available, and when the issue can be reported publicly. Unfortunately,
without a dedicated security and maintainer team it's difficult to give
reasonably short timeframe guarantees for this.


Bounties
--------

Crochet does not have any bug bounty program and cannot reward
security reports.