# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.decorators.tests.recording_management import (
    start_recording_scenario,
    end_recording_scenario,
    scenario_exists,
)


from ghosts.decorators.api_recorder import api_recorder, ApiRecorderController
from ghosts.decorators.tests.scenario import (
    ApiSuperClassDecorated,
    scenario_val,
    api_response,
)


@api_recorder
def what_can_beat(x, y, a='Ants', b='Bears'):
    return '{} {} can beat {} {}'.format(x, a, y, b)


def test_complex_input():
    scenario_name = 'test_complex_input'

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.acr.flushdb()

    start_recording_scenario(scenario_name)

    dog1 = what_can_beat(14, 3, 'Dogs', 'Dinosaurs')
    cat1 = what_can_beat(1, 13, 'Cats', 'Mice')
    cow1 = what_can_beat(20, 13, 'Cows', 'Mice')
    ant1 = what_can_beat(10000, 13, 'Ants', 'Pigs')

    end_recording_scenario(scenario_name)

    acr_remote.acr.flushdb()

    acr_remote.start_playingback()

    dog2 = what_can_beat(14, 3, 'Dogs', 'Dinosaurs')
    cat2 = what_can_beat(1, 13, 'Cats', 'Mice')
    cow2 = what_can_beat(20, 13, 'Cows', 'Mice')
    ant2 = what_can_beat(10000, 13, 'Antss', 'Pigs')

    assert dog2 == None

    acr_remote.load_scenario(scenario_name)

    dog3 = what_can_beat(14, 3, 'Dogs', 'Dinosaurs')
    cat3 = what_can_beat(1, 13, 'Cats', 'Mice')
    cow3 = what_can_beat(20, 13, 'Cows', 'Mice')
    ant3 = what_can_beat(10000, 13, 'Ants', 'Pigs')

    assert dog3 == dog1
    assert cat3 == cat1
    assert cow3 == cow1
    assert ant3 == ant1

    assert not dog3 == ant1
    assert not cat3 == cow1
    assert not cow3 == cat1
    assert not ant3 == dog1

    acr_remote.recorder_off()
