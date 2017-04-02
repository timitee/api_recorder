# -*- encoding: utf-8 -*-
from ghosts.api_recorder.api_controller import ApiRecorderController


def start_recording_scenario(site_name, scenario_name, pretty_print=False):
    """Flush old recording for the scenario. Start a new recording session."""
    acr_remote = ApiRecorderController(site_name, scenario_name, pretty_print)
    acr_remote.acr.flushdb()
    acr_remote.start_recording()

def start_healing_scenario(site_name, scenario_name, pretty_print=False):
    pause_recording_scenario(site_name, scenario_name, pretty_print=False)

def pause_recording_scenario(site_name, scenario_name, pretty_print=False):
    """Stop doing anything, but leave the current scenario in session."""
    acr_remote = ApiRecorderController(site_name, scenario_name, pretty_print)
    acr_remote.recorder_off()

def restart_recording_scenario(site_name, scenario_name, pretty_print=False):
    """Pickup a Recording."""
    acr_remote = ApiRecorderController(site_name, scenario_name, pretty_print)
    acr_remote.start_recording()

def end_and_save_scenario(site_name, scenario_name, pretty_print=False):
    """Recorder off. Build the "loader" or backup file."""
    acr_remote = ApiRecorderController(site_name, scenario_name, pretty_print)
    acr_remote.recorder_off()
    acr_remote.save_scenario()
    # if input('Good. {}:{} saved. Continue with next scenario? [*/n]'.format(site_name, scenario_name)) == 'n':
    #     return
    acr_remote.acr.flushdb()

def load_scenario(site_name, scenario_name, pretty_print=False):
    """Load a previously recorded data for this scenario. Start playback."""
    acr_remote = ApiRecorderController(site_name, scenario_name, pretty_print)
    acr_remote.acr.flushdb()
    acr_remote.load_scenario()
    acr_remote.start_playingback()

def pause_playback_scenario(site_name, scenario_name, pretty_print=False):
    pause_recording_scenario(site_name, scenario_name, pretty_print=False)

def restart_playback_scenario(site_name, scenario_name, pretty_print=False):
    """Flush old recording for the scenario. Start a new recording session."""
    acr_remote = ApiRecorderController(site_name, scenario_name, pretty_print)
    acr_remote.start_playingback()

def unload_scenario(site_name, scenario_name, pretty_print=False):
    """Recorder off. Flush this scenario."""
    acr_remote = ApiRecorderController(site_name, scenario_name, pretty_print)
    acr_remote.recorder_off()
    acr_remote.acr.flushdb()




def scenario_exists(site_name, scenario_name, pretty_print=False):
    """Check for recorded data for this scenario."""
    acr_remote = ApiRecorderController(site_name, scenario_name, pretty_print)
    return acr_remote.scenario_exists()
