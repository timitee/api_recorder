# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.ioioio.pinpoint import project_path
from ghosts.decorators.api_recorder import ApiRecorderController

scenario_name = 'test_api_mocking'


def test_making_mocks():

    acr_remote = ApiRecorderController(scenario_name)
    assert acr_remote.scenario == scenario_name

    # Flush the api db
    acr_remote.flush_scenario()

    acr_remote.start_recording()
    acr_remote.start_mocking()

    """Use the ApiMarshall and BpiMarshall from ghosts."""
    from ghosts.decorators.tests.scenario import (
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

    mocks_path = os.path.join(project_path(), 'automocks')
    module_name = 'mock_{}.py'.format(scenario_name)
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

    acr_remote.recorder_off()
    acr_remote.flush_scenario()
