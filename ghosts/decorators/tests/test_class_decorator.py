# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.decorators.api_recorder import ApiRecorderController
from ghosts.decorators.tests.scenario import (
    ApiClassDecorated,
    scenario_val,
    api_response,
)

scenario_name = 'test_class_decorator'

def test_service_when_off():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()
    m = ApiClassDecorated()
    c = ApiClassDecorated

    acr_remote.recorder_off()

    assert m.decorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm1', scenario_val)
    """Answers the question: Has the decorator interfered with it's normal
    behaviour? i.e. (from above) Are we "passing it on as normal"?"""

    acr_remote.recorder_off()
    acr_remote.flush_scenario()


def test_start_recording():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()
    m = ApiClassDecorated()
    c = ApiClassDecorated

    acr_remote.start_recording()

    assert m.decorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm1', scenario_val)
    """Answers the question: Has the decorator interfered with it's normal
    behaviour? i.e. (from above) Are we "passing it on as normal"?"""

    acr_remote.recorder_off()
    acr_remote.flush_scenario()


def test_start_playingback_on():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()
    m = ApiClassDecorated()
    c = ApiClassDecorated

    acr_remote.start_playingback()

    assert m.decorated_m(scenario_val) == None
    """Answers the question: When the recorder is attempting to play back
    method calls which haven't be made, does it return "none". """

    acr_remote.start_playingback()

    assert m.decorated_m(scenario_val) == None
    """Answers the question: When the recorder is attempting to play back
    method calls which haven't be made, does it return "none". """

    acr_remote.recorder_off()
    acr_remote.flush_scenario()


def test_record_playback():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()
    m = ApiClassDecorated()
    c = ApiClassDecorated

    acr_remote.start_recording()

    assert m.decorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm1', scenario_val)

    acr_remote.start_playingback()

    assert m.decorated_m(scenario_val) == api_response.format(c.__module__, c.__name__, 'm1', scenario_val)

    acr_remote.recorder_off()
    acr_remote.flush_scenario()
