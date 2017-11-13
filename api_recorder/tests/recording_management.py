# -*- encoding: utf-8 -*-
from api_recorder.api_controller import ApiRecorderController

class TheMC():
    """The Master control."""

    master_site = 'api_recorder'
    master_name = 'root'

    site = 'api_recorder'
    scenario = 'root'

    def __init__(self, site=None, scenario=None):
        if site:
            self.site = site
        if scenario:
            self.scenario = scenario

    def load(self, site, scenario):
        self.site = site
        self.scenario = scenario

    def master(self):
        self.load(self.master_site, self.master_name)

    def rec(self):
        start_recording_scenario(self.site, self.scenario)
    def heal(self):
        pause_recording_scenario(self.site, self.scenario)
    def pause(self):
        pause_recording_scenario(self.site, self.scenario)
    def unpause(self):
        unpause_recording_scenario(self.site, self.scenario)
    def save(self):
        end_and_save_scenario(self.site, self.scenario)

    def play(self):
        play_scenario(self.site, self.scenario)
    def suspend(self):
        suspend_playback_scenario(self.site, self.scenario)
    def resume(self):
        resume_playback_scenario(self.site, self.scenario)
    def eject(self):
        eject_scenario(self.site, self.scenario)

    def mock(self):
        start_mocking(self.site, self.scenario)
    def kind(self):
        stop_mocking(self.site, self.scenario)

    def sample(self, key):
        arc = ApiRecorderController(self.site, self.scenario)
        return arc.master_get_mock(key)

    def off(self):
        """Undestructive."""
        arc = ApiRecorderController(self.site, self.scenario)
        arc.recorder_off()
        arc.stop_mocking()
    def shutdown(self):
        """Destructive. Hard reboot."""
        arc = ApiRecorderController(self.site, self.scenario)
        arc.recorder_off()
        arc.stop_mocking()
        arc.acr.flushdb()
        arc.acr_settings.flushdb()
        arc.acr_counter.flushdb()


def start_recording_scenario(site_name, scenario_name, pretty_print=False):
    """Flush old recording for the scenario. Start a new recording session."""
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    arc.acr.flushdb()
    arc.start_recording()

def start_healing_scenario(site_name, scenario_name, pretty_print=False):
    pause_recording_scenario(site_name, scenario_name, pretty_print=False)

def pause_recording_scenario(site_name, scenario_name, pretty_print=False):
    """Stop doing anything, but leave the current scenario in session."""
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    arc.recorder_off()

def unpause_recording_scenario(site_name, scenario_name, pretty_print=False):
    """Pickup a Recording."""
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    arc.start_recording()

def end_and_save_scenario(site_name, scenario_name, pretty_print=False):
    """Recorder off. Build the "loader" or backup file."""
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    arc.recorder_off()
    arc.save_scenario()
    # if input('Good. {}:{} saved. Continue with next scenario? [*/n]'.format(site_name, scenario_name)) == 'n':
    #     return
    arc.acr.flushdb()

def play_mocking(site_name, scenario_name, pretty_print=False):
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    arc.acr.flushdb()
    arc.play_scenario()
    arc.start_playingback()
    arc.start_mocking()

def play_scenario(site_name, scenario_name, pretty_print=False):
    """Load a previously recorded data for this scenario. Start playback."""
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    arc.acr.flushdb()
    arc.play_scenario()
    arc.start_playingback()

def suspend_playback_scenario(site_name, scenario_name, pretty_print=False):
    pause_recording_scenario(site_name, scenario_name, pretty_print=False)

def resume_playback_scenario(site_name, scenario_name, pretty_print=False):
    """Flush old recording for the scenario. Start a new recording session."""
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    arc.start_playingback()

def eject_scenario(site_name, scenario_name, pretty_print=False):
    """Recorder off. Flush this scenario."""
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    arc.recorder_off()
    arc.acr.flushdb()


def start_mocking(site_name, scenario_name, pretty_print=False):
    """Starts writing mocks to a file. Call can still be recorded to the DB.
    Playbacks can be Mocked.
    """
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    arc.start_mocking()

def stop_mocking(site_name, scenario_name, pretty_print=False):
    """Stops writing mocks to a file. Call can still be recorded to the DB."""
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    arc.stop_mocking()


def scenario_exists(site_name, scenario_name, pretty_print=False):
    """Check for recorded data for this scenario."""
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    return arc.scenario_exists()



def power_down():
    """Check for recorded data for this scenario."""
    arc = ApiRecorderController(site_name, scenario_name, pretty_print)
    arc.recorder_off()
    arc.stop_mocking()
    arc.acr.flushdb()
