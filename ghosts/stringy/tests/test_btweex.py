# -*- encoding: utf-8 -*-
from ghosts.stringy.btweex import *
from ghosts.stringy.tests.major_general import major_general

enz = '; '
"""Default end string for the tests"""

compleex = major_general.format(enz=enz)
"""A complex string to test."""


def test_btweex_simple():

    simple = '<p>Hello</p>'

    assert 'Hello' == btweex(simple, '<p>', '</p>', False)

    assert simple == btweex(simple, '<p>', '</p>', True)



def expected(starz, stweex, preappend):
    """This returns the expected complete phrase of the test. Specify when your
    `btweex` call has preappend==True.
    """
    if preappend:
        return '{}{}{}'.format(starz, stweex, enz)
    else:
        return stweex

def test_expected():

    preappend = True
    starz = 'know'
    stweex = ' the kings of England'

    assert expected(starz, stweex, preappend) == '{}{}{}'.format(starz, stweex, enz)
    """The expected string will match the btweex string if correct: and
    preappend starz and enz.
    """

    preappend = False
    assert expected(starz, stweex, preappend) == stweex
    """The expected string will match the btweex string if correct: and
    preappend==False.
    """


def test_btweex_major_simple():

    preappend = True
    starz = 'know'
    stweex = ' the kings of England'

    assert btweex(compleex, starz, enz, preappend) == expected(starz, stweex, preappend)



def test_btweex_major_array():

    preappend = False
    starz = 'quote'
    stweexes = [
            ' the fights historical',
            ' in elegiacs all the crimes of Heliogabalus']

    results = btweexes(compleex, starz, enz, preappend, 0)

    assert results == stweexes



def test_btweex_no_starz():

    preappend = True
    starz = ''
    stweex = ' the kings of England'

    assert btweex(compleex, starz, enz, preappend) == ''



def test_btweex_no_enz():

    preappend = True
    starz = 'know'
    stweex = ' the kings of England'

    assert btweex(compleex, starz, '', preappend) == ''
