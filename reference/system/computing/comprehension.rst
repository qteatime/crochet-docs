Working with multiple values
============================

Lists, records, and other ways of combining multiple values
are a convenience, but sometimes we want to treat all of
these values uniformly and do things with them.

For most cases, Crochet's standard library for collections
provides a set of commands for different needs here: things
like transforming, filtering, or sorting collections. But
Crochet also has some lower level syntaxes for this that
can be useful from time to time.


The ``for .. in .. do ..`` syntax
---------------------------------

If you're familiar with other programming languages, you might
have seen things like "iterators" or "list comprehensions".
Crochet has a similar idea in its ``for .. in .. do ..``
syntax. It allows one to do something for each item of
a collection.

For example, consider the case where we have a list of
characters, and we want to show which book they appear
in. We could express this program as follows::

    let Characters = [
      [name -> "Alice", appears-in -> "Alice in Wonderland"],
      [name -> "Dorothy", appears-in -> "The Wizard of Oz"],
    ];

    for Character in Characters do
      show: "[Character.name] appears in [Character.appears-in].";
    end

This could output:

    Alice appears in Alice in Wonderland.

    Dorothy appears in The Wizard of Oz.

Here, for each item in the ``Characters`` collection, we will
execute this little program between the ``do`` and ``end`` words.
And each time we execute this program, the name ``Character`` will
be associated with one of the items in the collection. For lists,
the default behaviour is to go through the items in the order they
appear in the list.


Filtering items
'''''''''''''''

When using the ``for`` syntax, we can also specify which items we
don't want to do anything with, directly in the syntax itself. This
avoids having to use a condition within the program, and often makes
things easier to read.

For example, consider the case where we're showing the items in a
player inventory, but we only want to show the key story items---not
regular, consumable items the player could've got from one of the
shops along their way. We could achieve this with the following piece
of code::

    let Inventory = [
      new key-item(blue-booch),
      new consumable(potion, 10),
      new equipment(red-coat),
      new key-item(letter-from-alice),
    ];

    show: "You're carrying:";
    for Item in Inventory if Item is key-item do
      show: "A [Item name].";
    end

This could output:

    You're carrying:

    A blue brooch.

    A letter from Alice.

In this case, we'll still go through all of the items in the inventory,
but we'll only execute the body of the ``for`` syntax if the item we're
looking at is of the type ``key-item``. So we execute the body twice.
Once for ``blue-brooch`` and once for ``letter-from-alice``.


Combining collections
'''''''''''''''''''''

Sometimes we have several collections that we want to consider when
doing something. For example, let's say we have a list of keys and
a list of locked objects. The game wants to give the player a hint
that shows which keys can open which objects, but some keys can
open multiple things.

Here, what we really want is to go through every key, and then
for each locked object, verify if we can use that key to open it.
This can be achieved in Crochet by using multiple ``.. in ..``
clauses in the for syntax::

    let Keys = [red-key, golden-key, blue-key];
    let Objects = [music-box, desk-drawer, jewelry-box];

    for Key in Keys, Object in Objects if Key opens: Object do
      show: "[Key] can open [Object].";
    end

If the red-key the music box, the blue-key opens the desk drawer, and the golden-key
opens anything, then this could output:

    The red key can open the music box.

    The golden key can open the music box.

    The golden key can open the desk drawer.

    The golden key can open the jewelry box.

    The blue key can open the desk drawer.


We could also nest these ``for`` syntaxes for similar effect::

    for Key in Keys do
      for Object in Objects if Key opens: Object do
        show: "[Key] can open [Object]"
      end
    end

This has the same observable behaviour, but the resulting *value*
of this for expressions is slightly different.


Results of ``for`` syntaxes
'''''''''''''''''''''''''''

The ``for`` syntax isn't only used for doing things. It can also
be used to transform and filter a collection, yielding a new
collection as a result.

For example, if we have a list of numbers, like this::

    let Numbers = [1, 2, 3, 4, 5];

Then we can get the list of these numbers doubled using the ``for`` syntax::

    let Doubled = for Number in Numbers do Number * 2 end;

    // Equivalent to:
    [
      1 * 2,
      2 * 2,
      3 * 2,
      4 * 2,
      5 * 2
    ];

We can also filter the list, keeping only the even numbers, using the
``for`` syntax::

    let Even = for Number in Numbers if Number is-divisible-by: 2 do Number end;

    // Equivalent to:
    [2, 4]

And here's why this makes the choice of using multiple ``.. in ..`` clauses
in the for syntax a bit different from nesting them. Imagine we have a list
of characters, and then a list of locations. We want all combinations of
characters and locations, so we combine these lists with the ``for`` syntax::

    let Characters = ["Alice", "Dorothy"];

    let Locations = ["Hall", "Dinning Room", "Kitchen"];

    let Combined = for Character in Characters, Location in Locations do
                     "[Character] at the [Location]"
                   end;

By writing the program like this, combined will have the following value::

    [
      "Alice at the Hall",
      "Alice at the Dinning Room",
      "Alice at the Kitchen",

      "Dorothy at the Hall",
      "Dorothy at the Dinning Room",
      "Dorothy at the Kitchen",
    ];

But if we nest it, like so::

    for Character in Characters do
      for Location in Locations do
        "[Character] in the [Location]";
      end
    end

Then we end up with a slightly different list::

    [
      [
        "Alice at the Hall",
        "Alice at the Dinning Room",
        "Alice at the Kitchen",
      ],

      [
        "Dorothy at the Hall",
        "Dorothy at the Dinning Room",
        "Dorothy at the Kitchen",
      ],
    ];

So, in the first case, we get a flat list containing all of the combinations.
In the second case, we get a nested list containing the combinations. The
result more or less follows the form we choose to write the program.