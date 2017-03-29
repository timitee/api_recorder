# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.ioioio.pinpoint import projectfile_folder
from ghosts.decorators.api_recorder import ApiRecorderController


scenario_name = 'test_api_recorder'


def test_recorder_off():
    # Turn the fake API off and test it's off
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.recorder_off()
    assert acr_remote.run_mode == ApiRecorderController.RECORDING
    assert acr_remote.power == ApiRecorderController.POWER_OFF

def test_start_recording():
    # Turn the fake API off and test it's off
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.start_recording()
    assert acr_remote.run_mode == ApiRecorderController.RECORDING
    assert acr_remote.power == ApiRecorderController.POWER_ON

def test_start_playingback():
    # Turn the fake API off and test it's off
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.start_playingback()
    assert acr_remote.run_mode == ApiRecorderController.PLAYBACK
    assert acr_remote.power == ApiRecorderController.POWER_ON
    """The three tests above are to test this module's methods."""

def test_service_when_off():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()

    from ghosts.decorators.tests.scenario import (
                                                    ApiMarshall,
                                                    BpiMarshall,
                                                    api_response,
                                                    scenario_val,
                                                    )

    acr_remote.recorder_off()

    for c in [ApiMarshall, BpiMarshall]:

        m = c()

        assert m.decorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm1', scenario_val)
        assert m.undecorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm2', scenario_val)
        """Has the decorator interfered with it's normal behaviour? i.e. (from
        above) Are we "passing it on as normal"?

        __module__ and __name__ get formatted into the string being returned by
        the methods in this scenario. Our test will format the same string this
        end. During playback we will want to confirm api_recorder can
        distinguish between identical classes from different modules,   but for
        now we just want to make sure the deactivated decorator doesn't
        interfere with it's usual activity.

        :param scenario_val: Any reasonably unique constant value.

        `scenario_val` should be unusual enough to compare recording and playback;
        about the strength of a cheap pair of headphones.

        :param api_response: A string formatter.

        `api_response` is used by the methods `m1` and `m2` to format a
        consistent string response which we believe is unique according to its
        module, class, name + the call parameters. We happen to have those
        identities and values in advance. The method should return the same if
        playback isn't getting it's tapes mixed up.
        """


    acr_remote.recorder_off()
    acr_remote.flush_scenario()



def test_start_recording():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()

    from ghosts.decorators.tests.scenario import (
                                                    ApiMarshall,
                                                    BpiMarshall,
                                                    api_response,
                                                    scenario_val,
                                                    )

    acr_remote.start_recording()

    for c in [ApiMarshall, BpiMarshall]:

        m = c()

        assert m.decorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm1', scenario_val)
        assert m.undecorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm2', scenario_val)
        """When the recorder is recording, does it interfere with the return
        value?

        NB: We always test a decorated function against an undecorated one.
        """

    acr_remote.recorder_off()
    acr_remote.flush_scenario()



def test_start_playingback_on():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()

    from ghosts.decorators.tests.scenario import (
                                                    ApiMarshall,
                                                    BpiMarshall,
                                                    api_response,
                                                    scenario_val,
                                                    )

    acr_remote.start_playingback()


    for c in [ApiMarshall, BpiMarshall]:

        m = c()

        assert m.decorated_m(scenario_val) == None
        assert m.undecorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm2', scenario_val)
        """Answers the question: When the recorder is attempting to play back
        method calls which haven't be made, does it return "none". """


    acr_remote.recorder_off()
    acr_remote.flush_scenario()


def test_uniqueness_of_very_similar_classes():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()

    """First we use the ApiMarshall and BpiMarshall from ghosts."""
    from ghosts.decorators.tests.scenario import (
                                                    ApiMarshall,
                                                    BpiMarshall,
                                                    api_response,
                                                    scenario_val,
                                                    )

    acr_remote.start_recording()

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        m.decorated_m(scenario_val)
        m.undecorated_m(scenario_val)
        """We've already tested this, just need to record again."""


    acr_remote.start_playingback()

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        assert m.decorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm1', scenario_val)
        assert m.undecorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm2', scenario_val)
        """This is the first time we've tested playing back a value."""


    from example_ghosts.tests.scenario import ApiMarshall, BpiMarshall
    """Now we switch to ApiMarshall and BpiMarshall from a module in the
    example_ghosts project app."""

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        assert m.decorated_m(scenario_val) == None
        assert m.undecorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm2', scenario_val)
        """Passing means the decorator has spotted the difference between the
        two "decorated_m" methods in different apps."""

    acr_remote.start_recording()

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        m.decorated_m('something different')
        m.undecorated_m('something different')
        """Already tested; but this time we record something different."""

    acr_remote.start_playingback()

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        assert not m.decorated_m('something different') == api_response.format(c.__module__, c.__name__, 'm1', scenario_val)
        assert not m.undecorated_m('something different') == api_response.format(c.__module__, c.__name__, 'm2', scenario_val)
        """Passing means the decorator hasn't playedback the last "decorated_m"
        value in the other module."""

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        assert m.decorated_m('something different') == api_response.format(c.__module__, c.__name__, 'm1', 'something different')
        assert m.undecorated_m('something different') == api_response.format(c.__module__, c.__name__, 'm2', 'something different')
        """Passing means the decorator returned something different after all."""


    acr_remote.recorder_off()
    acr_remote.flush_scenario()


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

    mock_file_path = os.path.join(projectfile_folder(__file__), 'scenarios')
    module_name = 'mock_{}.py'.format(scenario_name)
    mock_file = os.path.join(mock_file_path, module_name)

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
