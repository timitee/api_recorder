# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.api_recorder.api_recorder import api_recorder
from ghosts.api_recorder.tests.recording_management import (
    start_recording_scenario,
    pause_recording_scenario,
    start_healing_scenario,
    restart_recording_scenario,
    end_and_save_scenario,
    scenario_exists,
    load_scenario,
    pause_playback_scenario,
    restart_playback_scenario,
    unload_scenario,
)
from ghosts.api_recorder.tests.scenario import (
    ApiSuperClassDecorated,
    scenario_val,
    api_response,
)

site_name = 'pyghosts'


@api_recorder
def dictionary_input(contact):
    return contact['id']


@api_recorder
def dictionary_list_input(contact_list, x):
    return contact_list[x]['id']


contact_a = {
    'id': 1,
    'name': 'Ant',
    'sex': 'Male'
}

contact_b = {
    'id': 2,
    'name': 'Bear',
    'sex': 'Female'
}

contact_c = {
    'id': 3,
    'name': 'Cat',
    'sex': 'Female'
}


def test_dictionary_input():

    scenario_name = 'test_dictionary_input'
    start_recording_scenario(site_name, scenario_name)

    ca1 = dictionary_input(contact_a)
    cb1 = dictionary_input(contact_b)
    cc1 = dictionary_input(contact_c)

    pause_recording_scenario(site_name, scenario_name)

    ca2 = dictionary_input(contact_a)
    cb2 = dictionary_input(contact_b)
    cc2 = dictionary_input(contact_c)

    end_and_save_scenario(site_name, scenario_name)

    load_scenario(site_name, scenario_name)

    ca2 = dictionary_input(contact_a)
    cb2 = dictionary_input(contact_b)
    cc2 = dictionary_input(contact_c)

    assert dictionary_input(contact_a) != ca2
    """ca2 was not recorded."""

    restart_recording_scenario(site_name, scenario_name)

    ca3 = dictionary_input(contact_a)
    cb3 = dictionary_input(contact_b)
    cc3 = dictionary_input(contact_c)

    assert ca3 == ca1
    """ca1 was recorded and restored."""

    unload_scenario(site_name, scenario_name)


def test_dictionary_list_input():

    scenario_name = 'test_dictionary_list_input'
    start_recording_scenario(site_name, scenario_name)

    contact_list = [contact_a, contact_b, contact_c]

    ca1 = dictionary_list_input(contact_list, 0)

    end_and_save_scenario(site_name, scenario_name)

    load_scenario(site_name, scenario_name)

    ca2 = dictionary_list_input(contact_list, 0)

    assert ca2 == ca1
    """ca2 was recorded."""

    contact_list = [contact_b, contact_a, contact_c]
    ca3 = dictionary_list_input(contact_list, 0)
    """ca2 was recovered with items in another order."""

    assert not ca3 == ca1
    """ca2 was recovered but it's in another index."""

    ca4 = dictionary_list_input(contact_list, 1)
    """ca2 was recovered with items in another order."""

    assert not ca4 == ca1
    """ca2 was recovered but it's in another index."""

    unload_scenario(site_name, scenario_name)


@api_recorder
def what_can_beat(x, y, a='Ants', b='Bears'):
    return '{} {} can beat {} {}'.format(x, a, y, b)


def test_complex_input():

    scenario_name = 'test_complex_input'
    start_recording_scenario(site_name, scenario_name)

    dog1 = what_can_beat(14, 3, a='Dogs', b='Dinosaurs')
    cat1 = what_can_beat(1, 13, a='Cats', b='Mice')
    cow1 = what_can_beat(20, 13, a='Cows', b='Mice')
    ant1 = what_can_beat(10000, 13, a='Ants', b='Pigs')

    end_and_save_scenario(site_name, scenario_name)

    load_scenario(site_name, scenario_name)

    dog2 = what_can_beat(15, 4, a='Dogs', b='Dinosaurs')
    cat2 = what_can_beat(2, 7, a='Cats', b='Mice')
    cow2 = what_can_beat(10, 7, a='Cows', b='Mice')
    ant2 = what_can_beat(99999, 7, a='Ants', b='Pigs')

    assert dog2 == None
    """Different input has not been recorded."""

    dog3 = what_can_beat(14, 3, a='Dogs', b='Dinosaurs')
    cat3 = what_can_beat(1, 13, a='Cats', b='Mice')
    cow3 = what_can_beat(20, 13, a='Cows', b='Mice')
    ant3 = what_can_beat(10000, 13, a='Ants', b='Pigs')

    assert dog3
    assert cat3
    assert cow3
    assert ant3
    """We have something other than "None"."""

    assert dog3 == dog1
    assert cat3 == cat1
    assert cow3 == cow1
    assert ant3 == ant1
    """Original recording recovered."""

    assert not dog3 == ant1
    assert not cat3 == cow1
    assert not cow3 == cat1
    assert not ant3 == dog1
    """They are not all the same."""

    dog4 = what_can_beat(14, 3, b='Dogs', a='Dinosaurs')
    cat4 = what_can_beat(1, 13, b='Cats', a='Mice')
    cow4 = what_can_beat(20, 13, b='Cows', a='Mice')
    ant4 = what_can_beat(10000, 13, b='Ants', a='Pigs')

    assert not dog4 == dog1
    assert not cat4 == cat1
    assert not cow4 == cow1
    assert not ant4 == ant1

    unload_scenario(site_name, scenario_name)
