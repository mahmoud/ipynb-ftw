# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

from collections import Mapping, Sequence, Set, ItemsView

try:
    from typeutils import make_sentinel
    _REMAP_EXIT = make_sentinel('_REMAP_EXIT')
except ImportError:
    _REMAP_EXIT = object()

def default_visit(path, key, value):
    # print('visit(%r, %r, %r)' % (path, key, value))
    return key, value


def default_enter(path, key, value):
    # print('enter(%r, %r)' % (key, value))
    try:
        iter(value)
    except TypeError:
        return value, False
    if isinstance(value, basestring):
        return value, False
    elif isinstance(value, Mapping):
        return value.__class__(), ItemsView(value)
    elif isinstance(value, Sequence):
        return value.__class__(), enumerate(value)
    elif isinstance(value, Set):
        return value.__class__(), enumerate(value)
    return value, False


def default_exit(path, key, old_parent, new_parent, new_items):
    # print('exit(%r, %r, %r, %r, %r)'
    #       % (path, key, old_parent, new_parent, new_items))
    ret = new_parent
    if isinstance(new_parent, Mapping):
        new_parent.update(new_items)
    elif isinstance(new_parent, Sequence):
        vals = [v for i, v in new_items]
        try:
            new_parent.extend(vals)
        except AttributeError:
            ret = new_parent.__class__(vals)  # tuples
    elif isinstance(new_parent, Set):
        vals = [v for i, v in new_items]
        try:
            new_parent.update(new_items)
        except AttributeError:
            ret = new_parent.__class__(vals)  # frozensets
    else:
        raise RuntimeError('unexpected iterable type: %r' % type(new_parent))
    return ret

    
def remap(root, visit=default_visit, enter=default_enter, exit=default_exit,
          **kwargs):
    """The remap ("recursive map") function is used to traverse and
    transform nested structures. Lists, tuples, sets, and dictionaries
    are just a few of the data structures commonly nested into
    heterogenous tree-like structures that are ubiquitous in
    programming. Unfortunately, Python's built-in ways to compactly
    manipulate collections are flat. For instance, list comprehensions
    may be fast and succinct, but they don't recurse, making it
    tedious to quickly apply changes to real-world data.
    Here's an example of removing all None-valued items from the data:
    >>> from pprint import pprint
    >>> reviews = {'Star Trek': {'TNG': 10, 'DS9': 8.5, 'ENT': None},
    ...            'Babylon 5': 6, 'Dr. Who': None}
    >>> pprint(remap(reviews, lambda p, k, v: v is not None))
    {'Babylon 5': 6, 'Star Trek': {'DS9': 8.5, 'TNG': 10}}
    Notice how both Nones have been removed despite the nesting in the
    dictionary. Not bad for a one-liner, and that's just the beginning.
    remap takes four main arguments: the object to traverse and three
    optional callables which determine how the remapped object will be
    created.
    Args:
        root: The target object to traverse. By default, remap
            supports iterables like :class:`list`, :class:`tuple`,
            :class:`dict`, and :class:`set`, but any object traversable by
            *enter* will work.
        visit (callable): This function is called on every item in
            *root*. It must accept three positional arguments, *path*,
            *key*, and *value*. *path* is simply a tuple of parents'
            keys. *visit* should return the new key-value pair. It may
            also return ``True`` as shorthand to keep the old item
            unmodified, or ``False`` to drop the item from the new
            structure. *visit* is called after *enter*, on the new parent.
            The *visit* function is called for every item in root,
            including duplicate items. For traversable values, it is
            called on the new parent object, after all its children
            have been visited. The default visit behavior simply
            returns the key-value pair unmodified.
        enter (callable): This function controls which items in *root*
            are traversed. It accepts the same arguments as *visit*: the
            path, the key, and the value of the current item. It returns a
            pair of the blank new parent, and an iterator over the items
            which should be visited. If ``False`` is returned instead of
            an iterator, the value will not be traversed.
            The *enter* function is only called once per unique value. The
            default enter behavior support mappings, sequences, and
            sets. Strings and all other iterables will not be traversed.
        exit (callable): This function determines how to handle items
            once they have been visited. It gets the same three
            arguments as the other functions -- *path*, *key*, *value*
            -- plus two more: the blank new parent object returned
            from *enter*, and a list of the new items, as remapped by
            *visit*.
            Like *enter*, the *exit* function is only called once per
            unique value. The default exit behavior is to simply add
            all new items to the new parent, e.g., using
            :meth:`list.extend` and :meth:`dict.update` to add to the
            new parent. Immutable objects, such as a :class:`tuple` or
            :class:`namedtuple`, must be recreated from scratch, but
            use the same type as the new parent passed back from the
            *enter* function.
        reraise_visit (bool): A pragmatic convenience for the *visit*
            callable. When set to ``False``, remap ignores any errors
            raised by the *visit* callback. Items causing exceptions
            are kept. See examples for more details.
    remap is designed to cover the majority of cases with just the
    *visit* callable. While passing in multiple callables is very
    empowering, remap is designed so very few cases should require
    passing more than one function.
    When passing *enter* and *exit*, it's common and easiest to build
    on the default behavior. Simply ``from boltons.iterutils import
    default_enter`` (or ``default_exit``), and have your enter/exit
    function call the default behavior before or after your custom
    logic.
    """
    # TODO: enter() return (False, items) to continue traverse but cancel copy?
    if not callable(visit):
        raise TypeError('visit expected callable, not: %r' % visit)
    if not callable(enter):
        raise TypeError('enter expected callable, not: %r' % enter)
    if not callable(exit):
        raise TypeError('exit expected callable, not: %r' % exit)
    reraise_visit = kwargs.pop('reraise_visit', True)
    if kwargs:
        raise TypeError('unexpected keyword arguments: %r' % kwargs.keys())

    path, registry, stack = (), {}, [(None, root)]
    new_items_stack = []
    while stack:
        key, value = stack.pop()
        id_value = id(value)
        if key is _REMAP_EXIT:
            key, new_parent, old_parent = value
            id_value = id(old_parent)
            path, new_items = new_items_stack.pop()
            value = exit(path, key, old_parent, new_parent, new_items)
            registry[id_value] = value
            if not new_items_stack:
                continue
        elif id_value in registry:
            value = registry[id_value]
        else:
            res = enter(path, key, value)
            try:
                new_parent, new_items = res
            except TypeError:
                # TODO: handle False?
                raise TypeError('enter should return a tuple of (new_parent,'
                                ' items_iterator), not: %r' % res)
            if new_items is not False:
                # traverse unless False is explicitly passed
                registry[id_value] = new_parent
                new_items_stack.append((path, []))
                if value is not root:
                    path += (key,)
                stack.append((_REMAP_EXIT, (key, new_parent, value)))
                if new_items:
                    stack.extend(reversed(list(new_items)))
                continue
        if visit is default_visit:
            # avoid function call overhead by inlining identity operation
            visited_item = (key, value)
        else:
            try:
                visited_item = visit(path, key, value)
            except:
                if reraise_visit:
                    raise
                visited_item = True
            if visited_item is False:
                continue  # drop
            elif visited_item is True:
                visited_item = (key, value)
            # TODO: typecheck?
            #    raise TypeError('expected (key, value) from visit(),'
            #                    ' not: %r' % visited_item)
        try:
            new_items_stack[-1][1].append(visited_item)
        except IndexError:
            raise TypeError('expected remappable root, not: %r' % root)
    return value

