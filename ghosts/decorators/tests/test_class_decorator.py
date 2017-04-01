# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.decorators.tests.recording_management import (
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
from ghosts.decorators.tests.scenario import (
    ApiSuperClassDecorated,
    scenario_val,
    api_response,
)

site_name = 'pyghosts'
scenario_name = 'test_class_decorator'


def test_class_decorator_when_off():

    scenario_name = 'test_class_decorator_when_off'
    start_recording_scenario(site_name, scenario_name)

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    end_and_save_scenario(site_name, scenario_name)

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Answers the question: Has the decorator interfered with it's normal
    behaviour? i.e. (from above) Are we "passing it on as normal"?"""


def test_class_decorator_recording():

    scenario_name = 'test_class_decorator_recording'
    start_recording_scenario(site_name, scenario_name)

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Answers the question: Has the decorator interfered with it's normal
    behaviour? i.e. (from above) Are we "passing it on as normal"?"""

    end_and_save_scenario(site_name, scenario_name)


def test_start_class_decorator_playingback():

    scenario_name = 'test_start_class_decorator_playingback'
    start_recording_scenario(site_name, scenario_name)

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    end_and_save_scenario(site_name, scenario_name)

    load_scenario(site_name, scenario_name)

    assert m.decorated_super(scenario_val) == None
    """Answers the question: When the recorder is attempting to play back
    method calls which haven't be made, does it return "none". """

    unload_scenario(site_name, scenario_name)


def test_record_playback():

    scenario_name = 'test_start_class_decorator_playingback'
    start_recording_scenario(site_name, scenario_name)

    m = ApiSuperClassDecorated()
    c = ApiSuperClassDecorated

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Recorded: ..."""

    end_and_save_scenario(site_name, scenario_name)

    load_scenario(site_name, scenario_name)

    assert m.decorated_super(scenario_val) == api_response.format(c.__module__, c.__name__, 'decorated_super', scenario_val)
    """Playedback: ..."""

    unload_scenario(site_name, scenario_name)
