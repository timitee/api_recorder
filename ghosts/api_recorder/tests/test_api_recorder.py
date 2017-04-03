# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.ioioio.pinpoint import projectfile_folder
from ghosts.api_recorder.tests.recording_management import (
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

site_name = 'pyghosts'


def test_service_when_off():

    scenario_name = 'test_service_when_off'
    end_and_save_scenario(site_name, scenario_name)

    from ghosts.api_recorder.tests.scenario import (
                                                    ApiMarshall,
                                                    BpiMarshall,
                                                    api_response,
                                                    scenario_val,
                                                    )


    for c in [ApiMarshall, BpiMarshall]:

        m = c()

        assert m.decorated_m(scenario_val) == api_response(c.__module__, c.__name__, 'decorated_m', scenario_val)
        assert m.undecorated_m(scenario_val) == api_response(c.__module__, c.__name__, 'undecorated_m', scenario_val)
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


def test_start_recording():

    scenario_name = 'test_start_recording'
    start_recording_scenario(site_name, scenario_name)

    from ghosts.api_recorder.tests.scenario import (
                                                    ApiMarshall,
                                                    BpiMarshall,
                                                    api_response,
                                                    scenario_val,
                                                    )


    for c in [ApiMarshall, BpiMarshall]:

        m = c()

        assert m.decorated_m(scenario_val) == api_response(c.__module__, c.__name__, 'decorated_m', scenario_val)
        assert m.undecorated_m(scenario_val) == api_response(c.__module__, c.__name__, 'undecorated_m', scenario_val)
        """When the recorder is recording, does it interfere with the return
        value?

        NB: We always test a decorated function against an undecorated one.
        """

    end_and_save_scenario(site_name, scenario_name)


def test_start_playingback_on():

    scenario_name = 'test_start_playingback_on'
    start_recording_scenario(site_name, scenario_name)

    from ghosts.api_recorder.tests.scenario import (
                                                    ApiMarshall,
                                                    BpiMarshall,
                                                    api_response,
                                                    scenario_val,
                                                    )

    end_and_save_scenario(site_name, scenario_name)


    play_scenario(site_name, scenario_name)

    for c in [ApiMarshall, BpiMarshall]:

        m = c()

        assert m.decorated_m(scenario_val) == None
        assert m.undecorated_m(scenario_val) == api_response(c.__module__, c.__name__, 'undecorated_m', scenario_val)
        """Answers the question: When the recorder is attempting to play back
        method calls which haven't be made, does it return "none". """

    eject_scenario(site_name, scenario_name)


def test_uniqueness_of_very_similar_classes():

    scenario_name = 'test_uniqueness_of_very_similar_classes'
    start_recording_scenario(site_name, scenario_name)

    """First we use the ApiMarshall and BpiMarshall from ghosts."""
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

    play_scenario(site_name, scenario_name)

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        assert m.decorated_m(scenario_val) == api_response(c.__module__, c.__name__, 'decorated_m', scenario_val)
        assert m.undecorated_m(scenario_val) == api_response(c.__module__, c.__name__, 'undecorated_m', scenario_val)
        """This is the first time we've tested playing back a value."""


    from example_ghosts.tests.scenario import ApiMarshall, BpiMarshall
    """Now we switch to ApiMarshall and BpiMarshall from a module in the
    example_ghosts project app."""

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        assert m.decorated_m(scenario_val) == None
        assert m.undecorated_m(scenario_val) == api_response(c.__module__, c.__name__, 'undecorated_m', scenario_val)
        """Passing means the decorator has spotted the difference between the
        two "decorated_m" methods in different apps - not playedback decorated."""

    eject_scenario(site_name, scenario_name)

    start_recording_scenario(site_name, scenario_name)

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        m.decorated_m('something different')
        m.decorated_m('something different')
        m.decorated_m('something different')
        m.undecorated_m('something different')
        """Already tested; but this time we record something different."""

    end_and_save_scenario(site_name, scenario_name)

    play_scenario(site_name, scenario_name)

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        assert not m.decorated_m('something different') == api_response(c.__module__, c.__name__, 'decorated_m', scenario_val)
        assert not m.undecorated_m('something different') == api_response(c.__module__, c.__name__, 'undecorated_m', scenario_val)
        """Passing means the decorator hasn't playedback the last "decorated_m"
        value in the other module."""

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        assert m.decorated_m('something different') == api_response(c.__module__, c.__name__, 'decorated_m', 'something different')
        assert m.undecorated_m('something different') == api_response(c.__module__, c.__name__, 'undecorated_m', 'something different')
        """Passing means the decorator returned something different after all."""

    eject_scenario(site_name, scenario_name)
