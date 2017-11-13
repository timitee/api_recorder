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
    start_mocking,
    stop_mocking,
)

site_name = 'api_recorder'

def mock_file_init(scenario_name):

    mocks_path = os.path.join(project_path(), 'automocks')
    module_name = 'mock_{}__{}.py'.format(site_name, scenario_name)
    mock_file = os.path.join(mocks_path, module_name)
    if os.path.exists(mock_file):
        os.remove(mock_file)
    return mock_file


def test_different_classes_mock_making():

    scenario_name = 'test_different_classes_mock_making'

    mock_file = mock_file_init(scenario_name)

    start_recording_scenario(site_name, scenario_name)

    start_mocking(site_name, scenario_name)

    """Use the ApiMarshall and BpiMarshall from api_recorder."""
    from api_recorder.tests.scenario import (
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

    stop_mocking(site_name, scenario_name)

    end_and_save_scenario(site_name, scenario_name)

    assert os.path.exists(mock_file)
    """Has our mock file been created?"""

    with open(mock_file, '+r') as mock_file:
        mocks = mock_file.read()

    assert 'ApiMarshall' in mocks
    assert 'BpiMarshall' in mocks
    assert 'decorated_m' in mocks
    assert scenario_val in mocks
    """Does our mock file have this def?"""

    stop_mocking(site_name, scenario_name)


def test_not_making_mocks():

    scenario_name = 'test_not_making_mocks'

    mock_file = mock_file_init(scenario_name)

    start_recording_scenario(site_name, scenario_name)

    """Use the ApiMarshall and BpiMarshall from api_recorder."""
    from api_recorder.tests.scenario import (
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

    stop_mocking(site_name, scenario_name)

    end_and_save_scenario(site_name, scenario_name)

    assert not os.path.exists(mock_file)
    """Has our mock file been created?"""




def test_save_recording_to_mocks():

    scenario_name = 'test_save_recording_to_mocks'

    mock_file = mock_file_init(scenario_name)

    start_recording_scenario(site_name, scenario_name)

    start_mocking(site_name, scenario_name)

    """Use the ApiMarshall and BpiMarshall from api_recorder."""
    from api_recorder.tests.scenario import ApiMarshall

    m = ApiMarshall()
    m.decorated_m('Test1')
    m.decorated_m('Test2')
    m.decorated_m('Test3')
    m.decorated_m('Test4')
    m.decorated_m('Test5')
    m.decorated_m('Test6')

    stop_mocking(site_name, scenario_name)
    end_and_save_scenario(site_name, scenario_name)

    assert os.path.exists(mock_file)
    """Has our mock file been created?"""

    with open(mock_file, '+r') as mock_file:
        mocks = mock_file.read()

    assert 'ApiMarshall' in mocks
    assert 'decorated_m' in mocks
    assert 'Test5' in mocks
    """Does our mock file have this def?"""

    stop_mocking(site_name, scenario_name)



def test_playback_mocking():

    scenario_name = 'test_playback_mocking'

    mock_file = mock_file_init(scenario_name)

    start_recording_scenario(site_name, scenario_name)

    stop_mocking(site_name, scenario_name)

    """Use the ApiMarshall and BpiMarshall from api_recorder."""
    from api_recorder.tests.scenario import ApiMarshall

    m = ApiMarshall()
    m.decorated_m('Test1')
    m.decorated_m('Test2')
    m.decorated_m('Test3')
    m.decorated_m('Test4')
    m.decorated_m('Test5')
    m.decorated_m('Test6')


    end_and_save_scenario(site_name, scenario_name)

    play_scenario(site_name, scenario_name)

    start_mocking(site_name, scenario_name)

    m = ApiMarshall()
    m.decorated_m('Test1')
    m.decorated_m('Test2')
    m.decorated_m('Test3')
    m.decorated_m('Test4')
    m.decorated_m('Test5')
    m.decorated_m('Test6')

    stop_mocking(site_name, scenario_name)

    eject_scenario(site_name, scenario_name)

    assert os.path.exists(mock_file)
    """Has our mock file been created?"""

    with open(mock_file, '+r') as mock_file:
        mocks = mock_file.read()

    assert 'ApiMarshall' in mocks
    assert 'decorated_m' in mocks
    assert 'Test5' in mocks
    """Does our mock file have this def?"""

    stop_mocking(site_name, scenario_name)
