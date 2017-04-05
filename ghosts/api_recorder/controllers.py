# -*- encoding: utf-8 -*-
from ghosts.api_recorder.api_controller import ApiRecorderController
from ghosts.api_recorder.controllers import *


class BaseController():

    _master_site = 'pyghosts'
    _master_scenario = 'root'

    _site = 'pyghosts'
    _scenario = 'anonymous'

    def __init__(self, site=None, scenario=None):
        if site:
            self._site = site
        if scenario:
            self._scenario = scenario

    @property
    def site(self):
        return self._site

    @property
    def scenario(self):
        return self._scenario

    @property
    def arm(self):
        return ApiRecorderController(self.site, self.scenario)


class TestController(BaseController):

    def switch_recording_scenario(site, scenario):
        """Switch to new scenario."""
        self._site = site
        self._scenario = scenario


    def start_recording_scenario(self):
        """Flush old recording for the scenario. Start a new recording session."""
        self.arm.acr.flushdb()
        self.arm.start_recording()

    def start_healing_scenario(self):
        pause_recording_scenario()

    def pause_recording_scenario(self):
        """Stop doing anything, but leave the current scenario in session."""
        self.arm.recorder_off()

    def unpause_recording_scenario(self):
        """Pickup a Recording."""
        self.arm.start_recording()

    def end_and_save_scenario(self):
        """Recorder off. Build the "loader" or backup file."""
        self.arm.recorder_off()
        self.arm.save_scenario()
        # if input('Good. {}:{} saved. Continue with next scenario? [*/n]'.format()) == 'n':
        #     return
        self.arm.acr.flushdb()

    def play_scenario(self):
        """Load a previously recorded data for this scenario. Start playback."""
        self.arm.acr.flushdb()
        self.arm.play_scenario()
        self.arm.start_playingback()

    def suspend_playback_scenario(self):
        pause_recording_scenario()

    def resume_playback_scenario(self):
        """Flush old recording for the scenario. Start a new recording session."""
        arm.start_playingback()

    def eject_scenario(self):
        """Recorder off. Flush this scenario."""
        self.arm.recorder_off()
        self.arm.acr.flushdb()

    def start_mocking(self):
        """Starts writing mocks to a file. Call can still be recorded to the DB.
        Playbacks can be Mocked.
        """
        self.arm.start_mocking()

    def stop_mocking(self):
        """Stops writing mocks to a file. Call can still be recorded to the DB."""
        self.arm.stop_mocking()

    def scenario_exists(self):
        """Check for recorded data for this scenario."""
        return self.arm.scenario_exists()


class SimpleController(TestController):
    """The Test controller simplified. By default: Stops and starts things on a
    "root" scenario."""

    def dj(self, site, scenario):
        self.switch_recording_scenario()

    def exists(self, site, scenario):
        self.scenario_exists()

    def rec(self):
        self.start_recording_scenario()
    def heal(self):
        self.pause_recording_scenario()
    def pause(self):
        self.pause_recording_scenario()
    def unpause(self):
        self.unpause_recording_scenario()
    def save(self):
        self.end_and_save_scenario()

    def play(self):
        self.play_scenario()
    def suspend(self):
        self.suspend_playback_scenario()
    def resume(self):
        self.resume_playback_scenario()
    def eject(self):
        self.eject_scenario()

    def mock(self):
        self.start_mocking()
    def kind(self):
        self.stop_mocking()

    def sample(self, key):
        return self.arm.get_mock(key)

    def off(self):
        """Undestructive."""
        self.arm.recorder_off()
        self.arm.stop_mocking()

    def shutdown(self):
        """Destructive. Hard reboot. No save."""
        self.off()
        self.arm.acr.flushdb()


class RootController(SimpleController):
    """The Master control; simplified. By default: Stops and starts things on a
    "root" scenario."""

    def __init__(self, password):
        if not password == 'letmein':
            raise Exception('Root password incorrect.')

    @property
    def site(self):
        return self._master_site

    @property
    def scenario(self):
        return self._master_scenario
