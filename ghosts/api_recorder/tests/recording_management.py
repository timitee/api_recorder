# -*- encoding: utf-8 -*-
from ghosts.api_recorder.api_controller import ApiRecorderController


def start_recording_scenario(site_name, scenario_name):
    """Flush old recording for the scenario. Start a new recording session."""
    acr_remote = ApiRecorderController(site_name, scenario_name)
    acr_remote.acr.flushdb()
    acr_remote.start_recording()

def start_healing_scenario(site_name, scenario_name):
    pause_recording_scenario(site_name, scenario_name)

def pause_recording_scenario(site_name, scenario_name):
    """Stop doing anything, but leave the current scenario in session."""
    acr_remote = ApiRecorderController(site_name, scenario_name)
    acr_remote.recorder_off()

def restart_recording_scenario(site_name, scenario_name):
    """Pickup a Recording."""
    acr_remote = ApiRecorderController(site_name, scenario_name)
    acr_remote.start_recording()

def end_and_save_scenario(site_name, scenario_name):
    """Recorder off. Build the "loader" or backup file."""
    acr_remote = ApiRecorderController(site_name, scenario_name)
    acr_remote.recorder_off()
    acr_remote.save_scenario()
    acr_remote.acr.flushdb()


def load_scenario(site_name, scenario_name):
    """Load a previously recorded data for this scenario. Start playback."""
    acr_remote = ApiRecorderController(site_name, scenario_name)
    acr_remote.acr.flushdb()
    acr_remote.load_scenario()
    acr_remote.start_playingback()

def pause_playback_scenario(site_name, scenario_name):
    pause_recording_scenario(site_name, scenario_name)

def restart_playback_scenario(site_name, scenario_name):
    """Flush old recording for the scenario. Start a new recording session."""
    acr_remote = ApiRecorderController(site_name, scenario_name)
    acr_remote.start_playingback()

def unload_scenario(site_name, scenario_name):
    """Recorder off. Flush this scenario."""
    acr_remote = ApiRecorderController(site_name, scenario_name)
    acr_remote.recorder_off()
    acr_remote.acr.flushdb()




def scenario_exists(site_name, scenario_name):
    """Check for recorded data for this scenario."""
    acr_remote = ApiRecorderController(site_name, scenario_name)
    return acr_remote.scenario_exists()
