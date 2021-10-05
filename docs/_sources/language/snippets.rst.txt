
How are names unique?
"""""""""""""""""""""

But how is a name unique? Well, within a package, Crochet does not allow one
to define two type entities with the same name. For example::

    type rectangle(width, height);
    type rectangle(origin, destination);

If we give Crochet a module that looks like the one above, Crochet will reject
it because the same name, ``rectangle``, is used in two different type entities.

Of course, applying this same rule to an entire program would be complicated.
It would require everyone writing Crochet modules to agree on not using the
same name as any other person---and how do you even do that when code can
be written by complete strangers?

So these rules only apply within a package. Across packages things are a bit
different. Package names themselves must be unique. This does run into some
similar problems---Crochet addresses parts of this with a naming convention
for packages. But once we have unique package names, we can make the name of
every entity unique by prefixing the local name, like ``rectangle`` above,
with the package name. So if we have ``my-package`` defining a ``rectangle``
type, the full name for the type would be ``my-package/rectangle``. A
different package could then define a type with name ``rectangle`` without
causing any confusion.


How are names unforgeable?
""""""""""""""""""""""""""

If one knows how the full name of an entity is constructed, doesn't that mean
anyone can construct them? Well, yes. Anyone can put together the package name
and the entity name to get the full name. It would be really bad for Crochet's
security if this meant they now could *use* that entity.

So when we say that "names" are unforgeable, what we really mean is that people
can't get access to something by just knowing how its full name works. So if
``my-package`` defines a type ``rectangle`` (with full name ``my-package/rectangle``),
a separate package, such as ``user-package`` can only use that name if it
has been granted access.

Consider a case where ``user-package`` contains the following module::

    type other-rectangle(width, height) is my-package/rectangle;

Intuitively, it looks like ``user-package`` has managed to "forge" (have access
to) ``my-package``'s ``rectangle`` type by just knowing how its full name is
constructed. But knowing the name is only half of the battle.

When Crochet loads this module, it needs to assign *meaning* to the name. And
in this case, in order to assign meaning to ``my-package/rectangle``, our
``user-package`` would need to have been granted access to ``my-package``.
We'll discuss what exactly "access" means when we discuss security and
capabilities in the next chapter.