# -*- encoding: utf-8 -*-
from ghosts.stringy.btwix import *
from ghosts.stringy.tests.major_general import major_general

enz = '; '
"""Default end string for the tests"""

compleex = major_general.format(enz=enz)
"""A complex string to test."""


def test_btwix_simple():

    simple = '<p>Hello</p>'

    assert 'Hello' == btwix(simple, '<p>', '</p>', False)

    assert simple == btwix(simple, '<p>', '</p>', True)



def expected(starz, stwix, preappend):
    """This returns the expected complete phrase of the test. Specify when your
    `btwix` call has preappend==True.
    """
    if preappend:
        return '{}{}{}'.format(starz, stwix, enz)
    else:
        return stwix

def test_expected():

    preappend = True
    starz = 'know'
    stwix = ' the kings of England'

    assert expected(starz, stwix, preappend) == '{}{}{}'.format(starz, stwix, enz)
    """The expected string will match the btwix string if correct: and
    preappend starz and enz.
    """

    preappend = False
    assert expected(starz, stwix, preappend) == stwix
    """The expected string will match the btwix string if correct: and
    preappend==False.
    """


def test_btwix_major_simple():

    preappend = True
    starz = 'know'
    stwix = ' the kings of England'

    assert btwix(compleex, starz, enz, preappend) == expected(starz, stwix, preappend)



def test_btwix_major_array():

    preappend = False
    starz = 'quote'
    stwixes = [
            ' the fights historical',
            ' in elegiacs all the crimes of Heliogabalus']

    results = btwixes(compleex, starz, enz, preappend, 0)

    assert results == stwixes



def test_btwix_no_starz():

    preappend = True
    starz = ''
    stwix = ' the kings of England'

    assert btwix(compleex, starz, enz, preappend) == ''



def test_btwix_no_enz():

    preappend = True
    starz = 'know'
    stwix = ' the kings of England'

    assert btwix(compleex, starz, '', preappend) == ''
