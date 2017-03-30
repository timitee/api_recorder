# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.ioioio.pinpoint import projectfile_folder
from ghosts.decorators.api_recorder import ApiRecorderController

scenario_name = 'test_api_recorder'


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

        assert m.decorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_m', scenario_val)
        assert m.undecorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'undecorated_m', scenario_val)
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

        assert m.decorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_m', scenario_val)
        assert m.undecorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'undecorated_m', scenario_val)
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
        assert m.undecorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'undecorated_m', scenario_val)
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
        assert m.decorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_m', scenario_val)
        assert m.undecorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'undecorated_m', scenario_val)
        """This is the first time we've tested playing back a value."""


    from example_ghosts.tests.scenario import ApiMarshall, BpiMarshall
    """Now we switch to ApiMarshall and BpiMarshall from a module in the
    example_ghosts project app."""

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        assert m.decorated_m(scenario_val) == None
        assert m.undecorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'undecorated_m', scenario_val)
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
        assert not m.decorated_m('something different') == api_response.format(c.__module__, c.__name__, 'decorated_m', scenario_val)
        assert not m.undecorated_m('something different') == api_response.format(c.__module__, c.__name__, 'undecorated_m', scenario_val)
        """Passing means the decorator hasn't playedback the last "decorated_m"
        value in the other module."""

    for c in [ApiMarshall, BpiMarshall]:
        m = c()
        assert m.decorated_m('something different') == api_response.format(c.__module__, c.__name__, 'decorated_m', 'something different')
        assert m.undecorated_m('something different') == api_response.format(c.__module__, c.__name__, 'undecorated_m', 'something different')
        """Passing means the decorator returned something different after all."""


    acr_remote.recorder_off()
    acr_remote.flush_scenario()
