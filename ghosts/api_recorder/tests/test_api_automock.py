# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.ioioio.pinpoint import project_path
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

site_name = 'pyghosts'


def test_making_mocks():

    scenario_name = 'test_making_mocks'
    start_recording_scenario(site_name, scenario_name)

    """Use the ApiMarshall and BpiMarshall from ghosts."""
    from ghosts.api_recorder.tests.scenario import (
                                                    ApiMarshall,
                                                    BpiMarshall,
                                                    api_response,
                                                    scenario_val,
                                                    )

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        m.decorated_m(scenario_val)
        m.undecorated_m(scenario_val)
        """We've already tested this, just need to record again."""

    end_and_save_scenario(site_name, scenario_name)


    mocks_path = os.path.join(project_path(), 'automocks')
    module_name = 'mock_{}__{}.py'.format(site_name, scenario_name)
    mock_file = os.path.join(mocks_path, module_name)

    assert os.path.exists(mock_file)
    """Has our mock file been created?"""

    with open(mock_file, '+r') as mock_file:
        mocks = mock_file.read()

    assert 'ApiMarshall' in mocks
    assert 'BpiMarshall' in mocks
    assert 'decorated_m' in mocks
    assert scenario_val in mocks
    """Does our mock file have this def?"""
