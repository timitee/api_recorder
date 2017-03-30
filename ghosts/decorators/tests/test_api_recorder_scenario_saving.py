# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.ioioio.pinpoint import project_path
from ghosts.decorators.api_recorder import ApiRecorderController
from ghosts.decorators.tests.scenario import (
    ApiSuperClassDecorated,
    ApiSubClassDecorated,
    scenario_val,
    api_response,
)


def test_api_recorder_scenario_switching():

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    acr_remote = ApiRecorderController('api_recorder_scenario1')
    assert acr_remote.scenario == 'api_recorder_scenario1'

    # Flush the api db
    acr_remote.flush_scenario()
    acr_remote.start_recording()


    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)

    acr_remote.start_playingback()

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Scenario 1 playsback value."""

    acr_remote = ApiRecorderController('api_recorder_scenario2')
    assert acr_remote.scenario == 'api_recorder_scenario2'
    acr_remote.flush_scenario()

    assert m.decorated_super(scenario_val) == None
    """Flushed Scenario 2 has no value."""

    acr_remote = ApiRecorderController('api_recorder_scenario1')
    assert acr_remote.scenario == 'api_recorder_scenario1'

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Scenario 1 continues to playsback value."""

    acr_remote.recorder_off()

def test_api_recorder_scenarios_saving():

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    acr_remote = ApiRecorderController('api_recorder_scenario1')
    assert acr_remote.scenario == 'api_recorder_scenario1'

    # Flush the api db
    acr_remote.flush_scenario()
    acr_remote.start_recording()

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Playback value."""

    acr_remote.save_scenario()

    assert os.path.exists('automocks/redis_api_recorder_scenario1.json')
    """Saved Scenario 1 backup."""

    with open('automocks/redis_api_recorder_scenario1.json') as f:
        api_recorder_scenario1 = f.read()

    acr_remote.flush_scenario()

    acr_remote.start_playingback()

    assert m.decorated_super(scenario_val) == None
    """Scenario 1 was flushed."""

    acr_remote = ApiRecorderController('api_recorder_scenario2')

    acr_remote.start_recording()

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Scenario 2 playsback value."""

    acr_remote.save_scenario()

    assert os.path.exists('automocks/redis_api_recorder_scenario2.json')
    """Saved Scenario 2 backup."""

    with open('automocks/redis_api_recorder_scenario2.json') as f:
        api_recorder_scenario2 = f.read()

    assert not api_recorder_scenario2 == api_recorder_scenario1
    assert not 'api_recorder_scenario2' in api_recorder_scenario1
    assert not 'api_recorder_scenario1' in api_recorder_scenario2
    """Saved scenarios are different."""

    acr_remote.recorder_off()


def test_api_recorder_scenarios_saving_load():

    acr_remote = ApiRecorderController('scenarios_saving_load')

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    acr_remote.start_recording()

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Recorded value."""

    acr_remote.start_playingback()

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Recorded value."""

    acr_remote.save_scenario()
    acr_remote.flush_scenario()

    assert m.decorated_super(scenario_val) == None
    """Recordign erased."""

    acr_remote.load_scenario()

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Recordign restored."""

    acr_remote.recorder_off()
