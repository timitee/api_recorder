# -*- encoding: utf-8 -*-
import os
import pytest


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
from ghosts.api_recorder.tests.scenario import (
    ApiSuperClassDecorated,
    ApiSubClassDecorated,
    scenario_val,
    api_response,
)

site_name = 'pyghosts'

def test_service_when_off():

    scenario_name = 'test_service_when_off'
    start_recording_scenario(site_name, scenario_name)

    super_class = ApiSuperClassDecorated()
    super_type = ApiSuperClassDecorated
    sub_class = ApiSubClassDecorated()
    sub_type = ApiSubClassDecorated

    end_and_save_scenario(site_name, scenario_name)

    assert sub_class.decorated_sub(scenario_val) == api_response(sub_type.__module__, sub_type.__name__, 'decorated_sub', scenario_val)
    assert super_class.decorated_super(scenario_val) == api_response(super_type.__module__, super_type.__name__, 'decorated_super', scenario_val)
    """Answers the question: Has the decorator interfered with it's normal
    behaviour? i.e. (from above) Are we "passing it on as normal"?"""


def test_start_recording():

    scenario_name = 'test_start_recording'
    start_recording_scenario(site_name, scenario_name)

    super_class = ApiSuperClassDecorated()
    super_type = ApiSuperClassDecorated
    sub_class = ApiSubClassDecorated()
    sub_type = ApiSubClassDecorated

    assert sub_class.decorated_sub(scenario_val) == api_response(sub_type.__module__, sub_type.__name__, 'decorated_sub', scenario_val)
    assert super_class.decorated_super(scenario_val) == api_response(super_type.__module__, super_type.__name__, 'decorated_super', scenario_val)
    """Answers the question: Has the decorator interfered with it's normal
    behaviour? i.e. (from above) Are we "passing it on as normal"?"""

    end_and_save_scenario(site_name, scenario_name)


def test_start_playingback_on():

    scenario_name = 'test_start_playingback_on'
    start_recording_scenario(site_name, scenario_name)

    super_class = ApiSuperClassDecorated()
    super_type = ApiSuperClassDecorated
    sub_class = ApiSubClassDecorated()
    sub_type = ApiSubClassDecorated

    end_and_save_scenario(site_name, scenario_name)

    play_scenario(site_name, scenario_name)

    assert sub_class.decorated_sub(scenario_val) == None
    assert super_class.decorated_super(scenario_val) == None
    """Answers the question: When the recorder is attempting to play back
    method calls which haven't be made, does it return "none". """

    eject_scenario(site_name, scenario_name)


def test_record_playback():

    scenario_name = 'test_record_playback'
    start_recording_scenario(site_name, scenario_name)

    super_class = ApiSuperClassDecorated()
    super_type = ApiSuperClassDecorated
    sub_class = ApiSubClassDecorated()
    sub_type = ApiSubClassDecorated


    assert sub_class.decorated_sub(scenario_val) == api_response(sub_type.__module__, sub_type.__name__, 'decorated_sub', scenario_val)
    assert super_class.decorated_super(scenario_val) == api_response(super_type.__module__, super_type.__name__, 'decorated_super', scenario_val)
    """Recording... """

    end_and_save_scenario(site_name, scenario_name)

    play_scenario(site_name, scenario_name)

    assert sub_class.decorated_sub(scenario_val) == api_response(sub_type.__module__, sub_type.__name__, 'decorated_sub', scenario_val)
    assert super_class.decorated_super(scenario_val) == api_response(super_type.__module__, super_type.__name__, 'decorated_super', scenario_val)
    """Plays back correctly. """

    eject_scenario(site_name, scenario_name)
