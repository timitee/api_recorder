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


def test_api_recorder_scenario_switching():

    scenario_name = 'api_recorder_scenario1'

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    start_recording_scenario(scenario_name)

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)

    end_recording_scenario(scenario_name)

    load_scenario(scenario_name)

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Scenario 1 playsback value."""

    unload_scenario(scenario_name)

    scenario_name = 'api_recorder_scenario2'

    start_recording_scenario(scenario_name)
    end_recording_scenario(scenario_name)
    load_scenario(scenario_name)

    assert m.decorated_super(scenario_val) == None
    """Flushed Scenario 2 has no value."""

    unload_scenario(scenario_name)

    scenario_name = 'api_recorder_scenario1'
    load_scenario(scenario_name)

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Scenario 1 continues to playsback value."""

    unload_scenario(scenario_name)


def test_api_recorder_scenarios_saving():

    scenario_name = 'api_recorder_scenario3'

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    start_recording_scenario(scenario_name)

    m.decorated_super(scenario_val) == None
    """Record value."""

    end_recording_scenario(scenario_name)

    assert os.path.exists('automocks/redis_api_recorder_scenario3.json')
    """Saved Scenario 3 backup."""

    with open('automocks/redis_api_recorder_scenario3.json') as f:
        api_recorder_scenario3 = f.read()

    scenario_name = 'api_recorder_scenario4'
    start_recording_scenario(scenario_name)

    m.decorated_super(scenario_val) == None
    """Record value."""

    end_recording_scenario(scenario_name)

    assert os.path.exists('automocks/redis_api_recorder_scenario4.json')
    """Saved Scenario 2 backup."""

    with open('automocks/redis_api_recorder_scenario4.json') as f:
        api_recorder_scenario4 = f.read()

    assert not api_recorder_scenario4 == api_recorder_scenario3
    assert not 'api_recorder_scenario4' in api_recorder_scenario3
    assert not 'api_recorder_scenario3' in api_recorder_scenario4
    """Saved scenarios are different."""



def test_api_recorder_scenarios_saving_load():

    scenario_name = 'scenarios_saving_load'

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    start_recording_scenario(scenario_name)

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Recorded value."""

    end_recording_scenario(scenario_name)
    load_scenario(scenario_name)

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Recorded value."""

    unload_scenario(scenario_name)

    restart_playback_scenario(scenario_name)

    assert m.decorated_super(scenario_val) == None
    """Recording unloaded."""

    load_scenario(scenario_name)

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Recordign restored."""

    unload_scenario(scenario_name)
