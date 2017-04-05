# -*- encoding: utf-8 -*-
"""Remote control Record/Playback of an api method's return values."""
import collections
import copy
import inspect
import os
import redis
import pprint
import json
import redisdl

from slugify import slugify
from ghosts.ioioio.pinpoint import project_path
from ghosts.stringy.btweex import btweex

pp = pprint.PrettyPrinter(indent=4)


def make_path_not_exists(make_path):
    if not os.path.exists(make_path):
        os.makedirs(make_path)
    open(os.path.join(make_path, '__init__.py'), 'w')
    return make_path


class ApiRecorderController(object):
    """Control what happens to methods which use the @api_recorder decorator."""

    mock_format = (''
                    '\n'
                    '{}'
                    '\n'
                    '    return {}'
                    '\n'
                    '    # :endmock:'
                    '\n')

    APR_MOCKING = 'acr.settings.mocking'
    APR_SCENARIO = 'acr.settings.scenario'
    APR_RUNMODE = 'acr.settings.run_mode'
    APR_POWER = 'acr.settings.power'
    POWER_OFF = 'RecorderOff'
    POWER_ON = 'RecorderOn'
    MOCKING_OFF = 'MockingOff'
    MOCKING_ON = 'MockingOn'
    RECORDING = 'Recording'
    PLAYBACK = 'PlayBack'
    """All the above are database keys to various settings."""

    db_num = 10
    settings_db = 11
    counter_db = 12

    pretty_print = False

    def __init__(self, site_name, scenario_name, pretty_print=False):
        """"""
        self.acr = redis.StrictRedis(host='localhost', port=6379, db=self.db_num)
        self.acr_settings = redis.StrictRedis(host='localhost', port=6379, db=self.settings_db)
        self.acr_counter = redis.StrictRedis(host='localhost', port=6379, db=self.counter_db)
        self.acr_settings.set(self.APR_SCENARIO, '{}__{}'.format(site_name, scenario_name))
        self.pretty_print = pretty_print

    @property
    def scenario(self):
        """The name of the recording sceranio."""
        scenario = self.acr_settings.get(self.APR_SCENARIO)
        if scenario:
            return scenario.decode('utf-8')
        else:
            return 'root'

    @property
    def run_mode(self):
        """Recording or Playback."""
        status = self.acr_settings.get(self.APR_RUNMODE)
        if status:
            return status.decode('utf-8')
        else:
            return ''

    @property
    def power(self):
        """The decorator does nothing when the power is Off."""
        power = self.acr_settings.get(self.APR_POWER)
        if power:
            return power.decode('utf-8')
        else:
            return ''


    @property
    def mocks(self):
        """Mocking is On or Off."""
        mocking_on = self.acr_settings.get(self.APR_MOCKING)
        if mocking_on:
            return mocking_on.decode('utf-8')
        else:
            return self.MOCKING_OFF


    def scene_key(self, key):
        return key #TODO: record synchronpusly'{}__{}'.format(self.scenario, key)


    def recorder_off(self):
        """Turn the fake API off and test it's Off."""
        self.acr_settings.set(self.scene_key(self.APR_POWER), self.POWER_OFF)
        self.acr_settings.set(self.scene_key(self.APR_RUNMODE), self.RECORDING)

    def start_recording(self):
        self.acr_counter.flushdb()
        """Turn the fake API On and test it's not in Recording mode."""
        self.acr_settings.set(self.scene_key(self.APR_POWER), self.POWER_ON)
        self.acr_settings.set(self.scene_key(self.APR_RUNMODE), self.RECORDING)

    def start_playingback(self):
        """Turn the fake API On and test for PlayBack mode."""
        self.acr_counter.flushdb()
        self.acr_settings.set(self.scene_key(self.APR_POWER), self.POWER_ON)
        self.acr_settings.set(self.scene_key(self.APR_RUNMODE), self.PLAYBACK)

    def start_mocking(self):
        """Turn the fake API On and test for PlayBack mode."""
        self.acr_settings.set(self.scene_key(self.APR_MOCKING), self.MOCKING_ON)

    def stop_mocking(self):
        """Turn the fake API On and test for PlayBack mode."""
        self.acr_settings.set(self.scene_key(self.APR_MOCKING), self.MOCKING_OFF)

    def build_mock_if_safe(self, key, package):
        if self.mocks == self.MOCKING_ON:
            self.build_mock(key, copy.deepcopy(package))

    def see_mock(self, key, package):
        """Returns a python Mock object of the data recorded."""

        recording = package.get('recording')

        method_name = 'def mock_{}__{}__{}__{}__{}():'.format(
            package.get('module_path').replace('module_path_', ''),
            package.get('class_name').replace('class_name_', ''),
            package.get('method_name').replace('method_name_', ''),
            '__'.join(package.get('vals')),
            package.get('call_sig'),
        )
        """And informative method name HASH appended for the Mock."""

        if self.pretty_print:
            pp_recording = pp.pformat(recording)
            """Pretty printed Mock def."""
        else:
            pp_recording = recording


        mock_def = self.mock_format.format(
                                method_name,
                                pp_recording
                                )

        return mock_def, method_name


    def build_mock(self, key, package):
        """Save a Mock object into the <mock_site_scenario_name>.py file. It will
overwrite any Mocks it finds with "identical" signatures. These will almost
certainly be the for the same call in the same recording sequence, say:

during recording:
    callorder(callX1, call_A1, callX3)

during playback:
    callorder(replay_A1, replayX1, replayX3)

replayX1 will get callX1's data
replayX3 will get callX3's data

Flaw?: Call order during playback the same. Test will pass. I think that's
right. The data is simply there to support the tests.
"""

        mock_def, method_name = self.see_mock(key, package)

        mocks_path = os.path.join(project_path(), 'automocks')
        make_path_not_exists(mocks_path)
        """Putting all mocks into an automocks folder - root project."""

        module_name = 'mock_{}.py'.format(self.scenario)
        module_path = os.path.join(mocks_path, module_name)



        if not os.path.exists(module_path):
            """No existing mocks file. Write new."""


            with open(module_path, "w") as mock_file:

                mock_file.write('# -*- encoding: utf-8 -*-')
                mock_file.write('')
                mock_file.write(mock_def)

        else:

            print('here')

            with open(module_path, 'r') as mock_file:
                mocks = mock_file.read()
            """Existing mocks file."""

            if mock_def in mocks:
                """Check for same definition. Return if unchanged."""
                return mock_def

            if method_name in mocks:
                """Check for same method name. Replace is present."""

                mock_exists = btweex(mocks, method_name, '# :endmock:', True)
                mocks.replace(mock_exists, mock_def)

            else:

                mocks += mock_def

            with open(module_path, "w") as mock_file:
                mock_file.write(mocks)
                """New mocks file."""

        return mock_def


    def fixjson(self, s):
        s = json.loads(json.dumps(eval(s)))
        return s


    def process_packages(self, _recording):
        """We may eventually need an entire suite of processors in and out - but for
        now this works with Flickr API.

        TODO: Write a processor for each api you work with - and wire it in.
        """
        if _recording:
            _recording = self.fixjson(_recording)

        return _recording


    def flush_scenario(self):
        """"""
        pass

    def play_scenario(self):
        """"""

        with open('automocks/redis_{}.json'.format(self.scenario), 'r') as f:
            json_text = f.read()

        redisdl.loads(json_text, db=self.db_num)

    def save_scenario(self):
        """"""

        json_text = redisdl.dumps(encoding='iso-8859-1', pretty=True, db=self.db_num, keys=self.scenario)

        mocks_path = os.path.join(project_path(), 'automocks')
        make_path_not_exists(mocks_path)
        """Putting all dbs into an automocks folder - root project."""

        with open('automocks/redis_{}.json'.format(self.scenario), 'w') as f:
            f.write(json_text)


    def scenario_exists(self):
        """"""

        return os.path.exists('automocks/redis_{}.json'.format(self.scenario))

    def set(self, key, package):
        """Expose the redis set method."""

        self.build_mock_if_safe(key, package)

        if self.RECORDING:
            scenario_packages = self.acr.get(self.scenario) or {}
            scenario_packages = self.process_packages(scenario_packages)

            scenario_packages[key] = package

            return self.acr.set(self.scenario, scenario_packages)

        return None


    def master_get_mock(self, key):
        """Returns the entire package we saved which contains metadata
        plus the recording."""

        package = self.master_get_package(key)

        return self.see_mock(key, package) if package else None


    def master_get_package(self, key):
        """Returns the entire package we saved which contains metadata
        plus the recording."""

        for scenario in self.acr.keys():
            scenario_packages = self.acr.get(scenario)
            scenario_packages = self.process_packages(scenario_packages)
            package = scenario_packages.get(key, None)
            if package:
                return package

        return None

    def get_package(self, key):
        """Returns the entire package we saved which contains metadata
        plus the recording."""

        scenario_packages = self.acr.get(self.scenario) or {}
        scenario_packages = self.process_packages(scenario_packages)

        return scenario_packages.get(key, None) if scenario_packages else None


    def get(self, key):
        """Handler for the redis get method, which isolates and returns only the
        recorded data from the saved package."""

        package = self.get_package(key)
        
        self.build_mock_if_safe(key, package)

        recording = package.get('recording', None) if package else None

        # if recording:
        #     self.build_mock_if_safe(key, package)

        return recording
