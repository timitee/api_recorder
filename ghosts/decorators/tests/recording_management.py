# -*- encoding: utf-8 -*-
from ghosts.decorators.api_recorder import ApiRecorderController


def start_recording_scenario(scenario_name):
    """Flush old recording for the scenario. Start a new recording session."""
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.flush_scenario()
    acr_remote.start_recording()


def end_recording_scenario(scenario_name):
    """Recorder off. Build the "loader" or backup file."""
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.recorder_off()
    acr_remote.save_scenario()


def scenario_exists(scenario_name):
    """Check for recorded data for this scenario."""
    acr_remote = ApiRecorderController(scenario_name)
    return acr_remote.scenario_exists()


def load_scenario(scenario_name):
    """Load a previously recorded data for this scenario. Start playback."""
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.load_scenario()
    acr_remote.start_playingback()


def end_scenario(scenario_name):
    """Recorder off. Flush this scenario."""
    acr_remote = ApiRecorderController(scenario_name)
    acr_remote.recorder_off()
    acr_remote.flush_scenario()
