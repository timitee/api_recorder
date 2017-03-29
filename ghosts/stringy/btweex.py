# -*- encoding: utf-8 -*-
"""
`btweex` finds an unknown substring which can been identified by a start and end
string.

::

    from ghosts.stringy.betweex import btweex

    'Hello' == btweex('<p>Hello</p>', '<p>', '</p>')

"""

def _btweex_calc(compleex, starz, enz, preappend=False, in_start=0):
    """Helper: Returns what it finds between two strings in a compleex string.
    Also returns a place to start looking for the next one. """


    start = compleex.find(starz, in_start) + len(starz) #if preappend else 0

    if not start:
        return '', 0

    end = compleex.find(enz, start) #+ len(enz) if preappend else 0

    if not end:
        return '', 0

    if (start or end) and end > start:
        stweex = compleex[start:end]
    else:
        return '', 0

    if preappend:
        stweex = '{}{}{}'.format(starz, stweex, enz)

    return stweex, end if end > in_start else 0


def btweex(compleex, starz, enz, preappend=False):
    """What's `btweex` two strings in a compleex string."""

    btwx_calc = _btweex_calc(compleex, starz, enz, preappend)
    stweex = btwx_calc[0]
    return stweex


def btweexes(compleex, starz, enz, preappend=False, start=0):
    """An array of `btweex`."""

    _between_array = []

    btwx_calc = _btweex_calc(compleex, starz, enz, preappend, start)
    stweex = btwx_calc[0]
    start = btwx_calc[1]
    """First attempt to find a btweex."""

    while (stweex and start > 0):

        _between_array.append(stweex)
        """Add each successful attempt to find a btweex."""

        btwx_calc = _btweex_calc(compleex, starz, enz, preappend, start)
        stweex = btwx_calc[0]
        start = btwx_calc[1]
        """Iterative attempts to find a btweex from the next start point."""

    return _between_array
