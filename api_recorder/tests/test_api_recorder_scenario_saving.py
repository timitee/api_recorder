# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.ioioio.pinpoint import project_path
from api_recorder.tests.recording_management import (
    start_recording_scenario,
    pause_recording_scenario,
    start_healing_scenario,
    unpause_recording_scenario,
    end_and_save_scenario,
    scenario_exists,
    play_scenario,
    suspend_playback_scenario,
    resume_playback_scenario,
    eject_scenario,
)
from api_recorder.tests.scenario import (
    ApiSuperClassDecorated,
    ApiSubClassDecorated,
    scenario_val,
    api_response,
)

site_name = 'api_recorder'

def test_api_recorder_scenario_switching():

    scenario_name = 'test_api_recorder_scenario_switching1'

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    start_recording_scenario(site_name, scenario_name)

    assert m.decorated_super(scenario_val) == api_response(c.__module__, c.__name__, 'decorated_super', scenario_val)

    end_and_save_scenario(site_name, scenario_name)

    play_scenario(site_name, scenario_name)

    assert m.decorated_super(scenario_val) == api_response(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Scenario 1 playsback value."""

    eject_scenario(site_name, scenario_name)

    scenario_name = 'test_api_recorder_scenario_switching2'

    start_recording_scenario(site_name, scenario_name)
    end_and_save_scenario(site_name, scenario_name)
    """Record "nothing" in this scenario."""

    play_scenario(site_name, scenario_name)
    """Load "nothing"."""

    assert m.decorated_super(scenario_val) == None
    """Flushed Scenario 2 has no value."""

    eject_scenario(site_name, scenario_name)

    scenario_name = 'test_api_recorder_scenario_switching1'
    play_scenario(site_name, scenario_name)

    assert m.decorated_super(scenario_val) == api_response(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Scenario 1 continues to playsback value."""

    eject_scenario(site_name, scenario_name)


def test_api_recorder_scenarios_saving():

    scenario_name = 'test_api_recorder_scenarios_saving1'

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    start_recording_scenario(site_name, scenario_name)

    m.decorated_super(scenario_val) == None
    """Record value."""

    end_and_save_scenario(site_name, scenario_name)

    assert os.path.exists('automocks/redis_{}__{}.json'.format(site_name, scenario_name))
    """Saved Scenario 3 backup."""

    with open('automocks/redis_{}__{}.json'.format(site_name, scenario_name)) as f:
        api_recorder_scenario3 = f.read()

    scenario_name = 'test_api_recorder_scenarios_saving2'
    start_recording_scenario(site_name, scenario_name)

    m.decorated_super(scenario_val) == None
    """Record value."""

    end_and_save_scenario(site_name, scenario_name)

    assert os.path.exists('automocks/redis_{}__{}.json'.format(site_name, scenario_name))
    """Saved Scenario 2 backup."""

    with open('automocks/redis_{}__{}.json'.format(site_name, scenario_name)) as f:
        api_recorder_scenario4 = f.read()

    assert not api_recorder_scenario4 == api_recorder_scenario3
    assert not api_recorder_scenario4 in api_recorder_scenario3
    assert not api_recorder_scenario3 in api_recorder_scenario4
    """Saved scenarios are different."""


def test_api_recorder_scenarios_saving_load():

    scenario_name = 'test_api_recorder_scenarios_saving_load'

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    start_recording_scenario(site_name, scenario_name)

    assert m.decorated_super(scenario_val) == api_response(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Recorded value."""

    end_and_save_scenario(site_name, scenario_name)

    play_scenario(site_name, scenario_name)

    assert m.decorated_super(scenario_val) == api_response(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Restored value."""

    eject_scenario(site_name, scenario_name)

    resume_playback_scenario(site_name, scenario_name)

    assert m.decorated_super(scenario_val) == None
    """Scenario is unloaded."""

    play_scenario(site_name, scenario_name)

    assert m.decorated_super(scenario_val) == api_response(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Recordign restored."""

    eject_scenario(site_name, scenario_name)
