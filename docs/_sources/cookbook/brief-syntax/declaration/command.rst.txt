``command``
===========

A command declaration introduces a new global command in the
application. It has many different syntaxes depending on which
features of the command one is using, and the name of the command.


Signatures
----------

Signatures define the name of the command, and can be postfix, prefix, binary,
keyword, or self-less keyword.


Postfix commands
''''''''''''''''

A postfix command ``_ name`` can be defined with::

    command Requirement name do
      // Implementation
    end

Or::

    command Requirement name = Expression;


Cast commands
'''''''''''''

A cast command ``_ as Type`` can be defined with::

    command Requirement as type-name do
      // Implementation
    end

The right hole of this command is always going to be a specific type,
and it's not possible to bind that to any variable.


Binary commands
'''''''''''''''

A binary command ``_ + _`` can be defined with::

    command Requirement + Requirement do
      // Implementation
    end

Or::

    command Requirement + Requirement = Expression;

The following is the complete list of valid binary names:

- ``_ <- _`` (store);
- ``_ and _``;
- ``_ or _``;
- ``_ === _`` (equals);
- ``_ =/= _`` (not equals);
- ``_ > _`` (greater than);
- ``_ >= _`` (greater or equal to);
- ``_ < _`` (less than);
- ``_ <= _`` (less or equal to);
- ``_ + _`` (plus);
- ``_ - _`` (minus);
- ``_ * _`` (times);
- ``_ / _`` (divided by);
- ``_ % _`` (remainder of a division);
- ``_ ** _`` (power);
- ``_ ++ _`` (juxtaposition, concatenation);


Prefix commands
'''''''''''''''

A prefix command ``not _`` can be defined with::

    command not Requirement do
      // Implementation
    end
  
Or::

    command not Requirement = Expression;

The following is the complete list of valid prefix names:

- ``not _``;


Keyword commands
''''''''''''''''

A keyword command ``_ and: _ then: _`` can be defined with::

    command Requirement and: Requirement then: Requirement do
      // Implementation
    end

Or::

    command Requirement and: Requirement then: Requirement =
      Expression;

Self-less keyword commands
''''''''''''''''''''''''''

A self-less keyword command ``and: _ then: _`` can be defined with::

    command and: Requirement then: Requirement do
      // Implementation
    end

Or::

    command and: Requirement then: Requirement =
      Expression;


Requirements
------------

Requirements define how a command can be triggered. They can either
be left out (no requirements exist to prevent the command from triggering),
or can be based on types and traits.


Ignored requirements
''''''''''''''''''''

An ignored requirement uses the ``_`` (underscore) syntax::

    command _ name do
      // Implementation
    end


Variable requirements
'''''''''''''''''''''

A variable requirement is simply a variable name, such as ``Variable``::

    command Variable name do
      // Implementation
    end


Type requirements
'''''''''''''''''

A requirement that the value is of type ``good`` has syntax::

    command (Requirement is good) name do
      // Implementation
    end


Trait requirements
''''''''''''''''''

A requirement that the value has a trait ``trait-a``, and ``trait-b`` has
syntax::

    command (Requirement has trait-a, trait-b) name do
      // Implementation
    end

Type and trait requirements
'''''''''''''''''''''''''''

Combined type and trait requirements has the syntax::

    command (Requirement is good has trait-a, trait-b) name do
      // Implementation
    end


Contracts
---------

Contracts define conditions that must be true before the execution of
the command (pre-conditions), and after the execution of the command
(post-conditions).


Pre-conditions
''''''''''''''

A pre-condition is introduced by the ``requires`` keyword, and contains
any number of ``name :: Expression`` contracts::

    command Variable name
    requires
      first-condition :: Variable > 0,
      second-condition :: Variable < 30
    do
      // Implementation
    end

Post-conditions
'''''''''''''''

A post-condition is introduced by the ``ensures`` keyword, and contains
any number of ``name :: Expression`` contracts. It can use the ``return``
value::

    command Variable name
    ensures
      first-condition :: Variable < return,
      second-condition :: return < 100
    do
      // Implementation
    end


Test blocks
-----------

A test block is a convenience for writing example-based tests for the
command. It has the following syntax::

    command Variable name do
      // Implementation
    test
      assert 5 name === 10;
    end


Documentation comment
---------------------

Commands may have a preceding documentation comment with the syntax::

    /// This is a documentation comment
    /// And it spans
    /// Multiple lines
    ///
    command _ name do
      // Implementation
    end


Example
-------

::

    command (Items is list) separated-list do
      condition
        when Items is-empty => "";
        when Items count === 1 => "[Items first]";
        when Items count === 2 => "[Items at: 1], and [Items at: 2]";
        otherwise do
          "[Items first], [Items rest separated-list]";
        end
      end
    test
      assert [] separated-list flatten-into-plain-text === "";
      assert ["a", "b"] separated-list flatten-into-plain-text === "a, and b";
    end

