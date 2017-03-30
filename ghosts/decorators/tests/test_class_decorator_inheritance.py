# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.decorators.api_recorder import ApiRecorderController
from ghosts.decorators.tests.scenario import (
    ApiSuperClassDecorated,
    ApiSubClassDecorated,
    scenario_val,
    api_response,
)

scenario_name = 'test_class_inherit'


def test_service_when_off():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()
    super_class = ApiSuperClassDecorated()
    super_type = ApiSuperClassDecorated
    sub_class = ApiSubClassDecorated()
    sub_type = ApiSubClassDecorated

    acr_remote.recorder_off()

    assert sub_class.decorated_sub(scenario_val) == api_response.format(sub_type.__module__, sub_type.__name__, 'decorated_sub', scenario_val)
    assert super_class.decorated_super(scenario_val) == api_response.format(super_type.__module__, super_type.__name__, 'decorated_super', scenario_val)
    """Answers the question: Has the decorator interfered with it's normal
    behaviour? i.e. (from above) Are we "passing it on as normal"?"""

    acr_remote.recorder_off()
    acr_remote.flush_scenario()


def test_start_recording():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()
    super_class = ApiSuperClassDecorated()
    super_type = ApiSuperClassDecorated
    sub_class = ApiSubClassDecorated()
    sub_type = ApiSubClassDecorated

    acr_remote.start_recording()

    assert sub_class.decorated_sub(scenario_val) == api_response.format(sub_type.__module__, sub_type.__name__, 'decorated_sub', scenario_val)
    assert super_class.decorated_super(scenario_val) == api_response.format(super_type.__module__, super_type.__name__, 'decorated_super', scenario_val)
    """Answers the question: Has the decorator interfered with it's normal
    behaviour? i.e. (from above) Are we "passing it on as normal"?"""

    acr_remote.recorder_off()
    acr_remote.flush_scenario()


def test_start_playingback_on():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()
    super_class = ApiSuperClassDecorated()
    super_type = ApiSuperClassDecorated
    sub_class = ApiSubClassDecorated()
    sub_type = ApiSubClassDecorated

    acr_remote.start_playingback()

    assert sub_class.decorated_sub(scenario_val) == None
    assert super_class.decorated_super(scenario_val) == None
    """Answers the question: When the recorder is attempting to play back
    method calls which haven't be made, does it return "none". """

    acr_remote.start_playingback()

    assert sub_class.decorated_sub(scenario_val) == None
    assert super_class.decorated_super(scenario_val) == None
    """Answers the question: When the recorder is attempting to play back
    method calls which haven't be made, does it return "none". """

    acr_remote.recorder_off()
    acr_remote.flush_scenario()


def test_record_playback():

    # Flush the api db
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()
    super_class = ApiSuperClassDecorated()
    super_type = ApiSuperClassDecorated
    sub_class = ApiSubClassDecorated()
    sub_type = ApiSubClassDecorated

    acr_remote.start_recording()

    assert sub_class.decorated_sub(scenario_val) == api_response.format(sub_type.__module__, sub_type.__name__, 'decorated_sub', scenario_val)
    assert super_class.decorated_super(scenario_val) == api_response.format(super_type.__module__, super_type.__name__, 'decorated_super', scenario_val)

    acr_remote.start_playingback()

    assert sub_class.decorated_sub(scenario_val) == api_response.format(sub_type.__module__, sub_type.__name__, 'decorated_sub', scenario_val)
    assert super_class.decorated_super(scenario_val) == api_response.format(super_type.__module__, super_type.__name__, 'decorated_super', scenario_val)

    acr_remote.recorder_off()
    acr_remote.flush_scenario()
