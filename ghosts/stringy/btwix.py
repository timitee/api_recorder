# -*- encoding: utf-8 -*-
"""
`btwix` finds an unknown substring which can been identified by a start and end
string.

::

    from ghosts.stringy.betweex import btwix

    'Hello' == btwix('<p>Hello</p>', '<p>', '</p>')

"""

def _btwix_calc(compleex, starz, enz, preappend=False, in_start=0):
    """Helper: Returns what it finds between two strings in a compleex string.
    Also returns a place to start looking for the next one. """

    start = compleex.find(starz, in_start) + len(starz)

    if not start:
        return ('', 0)

    end = compleex.find(enz, start)

    if not end:
        return ('', 0)

    if (start or end) and end > start:
        stwix = compleex[start:end]
    else:
        return ('', 0)

    if preappend:
        stwix = '{}{}{}'.format(starz, stwix, enz)

    return (stwix, end if end > in_start else 0)


def btwix(compleex, starz, enz, preappend=False):
    """What string is `btwix` two strings in a compleex string."""

    btwx_calc = _btwix_calc(compleex, starz, enz, preappend)
    stwix = btwx_calc[0]
    return stwix


def btwixes(compleex, starz, enz, preappend=False, start=0):
    """A `btwix` list."""

    btwix_list = []

    btwx_calc = _btwix_calc(compleex, starz, enz, preappend, start)
    stwix = btwx_calc[0]
    start = btwx_calc[1]
    """First attempt to find a btwix."""

    while (stwix and start > 0):

        btwix_list.append(stwix)
        """Add each successful attempt to find a btwix."""

        btwx_calc = _btwix_calc(compleex, starz, enz, preappend, start)
        stwix = btwx_calc[0]
        start = btwx_calc[1]
        """Iterative attempts to find a btwix from the next start point."""

    return btwix_list
