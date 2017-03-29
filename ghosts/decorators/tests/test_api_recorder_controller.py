# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.decorators.api_recorder import ApiRecorderController

scenario_name = 'test_api_recorder_controller'


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

def test_start_mocking():
    # Turn the fake API off and test it's off
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.start_mocking()
    assert acr_remote.mocks == True

def test_stop_mocking():
    # Turn the fake API off and test it's off
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.stop_mocking()
    assert acr_remote.mocks == False
