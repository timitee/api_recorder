# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.decorators.tests.recording_management import (
    start_recording_scenario,
    end_recording_scenario,
    scenario_exists,
    start_healing_scenario,
    restart_recording_scenario,
    load_scenario,
    unload_scenario,
    restart_playback_scenario,
    pause_playback_scenario,
)



from ghosts.decorators.api_recorder import api_recorder, ApiRecorderController
from ghosts.decorators.tests.scenario import (
    ApiSuperClassDecorated,
    scenario_val,
    api_response,
)



@api_recorder
def dictionary_input(contact):
    return contact['id']


def test_dictionary_input():
    scenario_name = 'test_dictionary_input'

    start_recording_scenario(scenario_name)

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

    ca1 = dictionary_input(contact_a)
    cb1 = dictionary_input(contact_b)
    cc1 = dictionary_input(contact_c)

    end_recording_scenario(scenario_name)
    unload_scenario(scenario_name)

    ca2 = dictionary_input(contact_a)
    cb2 = dictionary_input(contact_b)
    cc2 = dictionary_input(contact_c)

    restart_playback_scenario(scenario_name)

    assert dictionary_input(contact_a) != ca2

    load_scenario(scenario_name)

    ca3 = dictionary_input(contact_a)
    cb3 = dictionary_input(contact_b)
    cc3 = dictionary_input(contact_c)

    assert ca3 == ca1
    assert cb3 == cb1
    assert cc3 == cc1

    unload_scenario(scenario_name)
    end_recording_scenario(scenario_name)



@api_recorder
def what_can_beat(x, y, a='Ants', b='Bears'):
    return '{} {} can beat {} {}'.format(x, a, y, b)


def test_complex_input():
    scenario_name = 'test_complex_input'

    start_recording_scenario(scenario_name)

    dog1 = what_can_beat(14, 3, a='Dogs', b='Dinosaurs')
    cat1 = what_can_beat(1, 13, a='Cats', b='Mice')
    cow1 = what_can_beat(20, 13, a='Cows', b='Mice')
    ant1 = what_can_beat(10000, 13, a='Ants', b='Pigs')

    end_recording_scenario(scenario_name)
    unload_scenario(scenario_name)

    restart_playback_scenario(scenario_name)

    dog2 = what_can_beat(14, 3, a='Dogs', b='Dinosaurs')
    cat2 = what_can_beat(1, 13, a='Cats', b='Mice')
    cow2 = what_can_beat(20, 13, a='Cows', b='Mice')
    ant2 = what_can_beat(10000, 13, a='Antss', b='Pigs')

    assert dog2 == None

    load_scenario(scenario_name)

    dog3 = what_can_beat(14, 3, a='Dogs', b='Dinosaurs')
    cat3 = what_can_beat(1, 13, a='Cats', b='Mice')
    cow3 = what_can_beat(20, 13, a='Cows', b='Mice')
    ant3 = what_can_beat(10000, 13, a='Ants', b='Pigs')

    assert dog3 == dog1
    assert cat3 == cat1
    assert cow3 == cow1
    assert ant3 == ant1

    assert not dog3 == ant1
    assert not cat3 == cow1
    assert not cow3 == cat1
    assert not ant3 == dog1

    dog4 = what_can_beat(14, 3, b='Dogs', a='Dinosaurs')
    cat4 = what_can_beat(1, 13, b='Cats', a='Mice')
    cow4 = what_can_beat(20, 13, b='Cows', a='Mice')
    ant4 = what_can_beat(10000, 13, b='Ants', a='Pigs')

    assert not dog4 == dog1
    assert not cat4 == cat1
    assert not cow4 == cow1
    assert not ant4 == ant1

    unload_scenario(scenario_name)
