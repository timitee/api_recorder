# -*- encoding: utf-8 -*-
"""Record/Playback an api method's return values.

api_recorder is an ambitious attempt to create a method @decorator which can
record, into a database, the return value(s) keyed against the method's identity
and the parameters. You know, like a VCR for python functions, except no one
knows what a VCR is. In this way you could write light api wrappers to consume a
live api and record the returning json responses. These stored responses can
then be played back in tests or when you don't have access to the api.

- Decorate your api wrappers.
    - Write your tests; making all the calls you want to test at least once.
    - Set it up so that your test errors are ignored.
    - Run your tests with "RecorderOn" mode on.

    Or;

    - Run a scenario with "RecorderOn" mode on.

- Develop your code speedily in "PlayBack" mode against the test data captured.
    - Reconnect and rerecord any time.
    - Package and archive your recordings. < TODO:

**Usage**

::

    from ghosts.ioioio.pinpoint import projectfile_folder
    from ghosts.decorators.api_recorder import ApiRecorderController, api_recorder

    acr_remote = ApiRecorderController('Scenario Name')

    @api_recorder
    def worthy(important):
        return important

    acr_remote.start_recording()
    acr_remote.start_mocking()

    being_recorded = worthy('I wrote this program didn\'t I!')
    being_recorded = worthy('I did!')
    being_recorded = worthy('Me!')

    start_playingback()

    listening_to_playback = worthy('Me!')

    assert listening_to_playback == being_recorded


This last assertion might seem obvious, but after calling `start_recording`
@api_recorder stores the return value of the method before passing it on as
normal.

After calling  `start_playingback` the @api_recorder decorator simply maps the
same variables + the signature of the method to retrieve (remember, if you like)
the last lot of data the method returned. Keyed against an api method this would
let you run tests against a set of known responses.

Technically it could be made to handle any serialable method return, but what
would be the point of recording an local method - except to see whether it
changes? I'm using it for an xml-rpc driven api and Flickr's json engine which I
working against for a client and personal project respectively.

I already have all the python low level nodes or plugs into the various api
methods - effectively a thin layer over 3rd party xml-rpc clients and flickrap
to decorate and test the feasibility.

TODO: Make @api_automock decorator separate.
"""
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

    def __init__(self, scenario):
        """"""
        self.acr = redis.StrictRedis(host='localhost', port=6379, db=10)
        self.acr_settings = redis.StrictRedis(host='localhost', port=6379, db=11)
        self.acr_settings.set(self.APR_SCENARIO, scenario)


    @property
    def scenario(self):
        """The name of the recording sceranio."""
        scenario = self.acr_settings.get(self.APR_SCENARIO)
        if scenario:
            return scenario.decode('utf-8')
        else:
            return ''

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
        mock = self.acr_settings.get(self.APR_MOCKING)
        if mock:
            return mock.decode('utf-8')
        else:
            return self.MOCKING_OFF



    def recorder_off(self):
        """Turn the fake API off and test it's Off."""
        self.acr_settings.set(self.APR_POWER, self.POWER_OFF)
        self.acr_settings.set(self.APR_RUNMODE, self.RECORDING)

    def start_recording(self):
        """Turn the fake API On and test it's not in Recording mode."""
        self.acr_settings.set(self.APR_POWER, self.POWER_ON)
        self.acr_settings.set(self.APR_RUNMODE, self.RECORDING)

    def start_playingback(self):
        """Turn the fake API On and test for PlayBack mode."""
        self.acr_settings.set(self.APR_POWER, self.POWER_ON)
        self.acr_settings.set(self.APR_RUNMODE, self.PLAYBACK)

    def start_mocking(self):
        """Turn the fake API On and test for PlayBack mode."""
        self.acr_settings.set(self.APR_MOCKING, self.MOCKING_ON)

    def stop_mocking(self):
        """Turn the fake API On and test for PlayBack mode."""
        self.acr_settings.set(self.APR_MOCKING, self.MOCKING_OFF)


    def build_mock(self, key, val):
        """Build a Mock object."""

        recording = val.get('recording')

        mocks_path = os.path.join(project_path(), 'automocks')
        make_path_not_exists(mocks_path)
        """Putting all mocks into an automocks folder - root project."""

        module_name = 'mock_{}.py'.format(self.scenario)
        module_path = os.path.join(mocks_path, module_name)

        method_name = 'def mock_{}__{}__{}__{}():'.format(
            val.get('module_path').replace('module_path_', ''),
            val.get('class_name').replace('class_name_', ''),
            val.get('method_name').replace('method_name_', ''),
            ''.join(val.get('vals')),
        )
        """Unique-ish method name for the mock."""

        mock_def = self.mock_format.format(
                                method_name,
                                pp.pformat(recording)
                                )
        """Pretty printed mock def."""

        if not os.path.exists(module_path):
            """No cxisting mocks file. Write new."""

            with open(module_path, "w") as mock_file:

                mock_file.write('# -*- encoding: utf-8 -*-')
                mock_file.write('')
                mock_file.write(mock_def)

        else:

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


    def process_recording(self, _recording):
        """We may eventually need an entire suite of processors in and out - but for
        now this works with Flickr API.

        TODO: Write a processor for each api you work with - and wire it in.
        """
        if _recording:
            _recording = self.fixjson(_recording)

        return _recording


    def scenario_keys(self):
        """"""
        return self.acr.keys()


    def flush_scenario(self):
        """"""

        with open('automocks/scenario_{}.json'.format(self.scenario or 'api_recorder'), 'w') as f:
            redisdl.dump(f, encoding='iso-8859-1', pretty=True)

        return self.acr.flushdb()


    def mocks_scenario(self):

        kys = self.scenario_keys()
        for key, val in kys:
            self.build_mock(key, val)
        pass


    def set(self, key, val):
        """Expose the redis set method."""

        if self.mocks:
            """Create a mock object with the current data."""

            self.build_mock(key, copy.deepcopy(val))

        return self.acr.set(key, val)


    def get_package(self, key):
        """Returns the entire package we saved which contains metadata
        plus the recording."""

        package = self.process_recording(self.acr.get(key))
        return package


    def get(self, key):
        """Handler for the redis get method, which isolates and returns only the
        recorded data from the saved package."""

        package = self.get_package(key)
        return package.get('recording', None) if package else None


acr_remote = ApiRecorderController('root')


def api_recorder(func):
    """Record/Playback a method output keyed to input."""

    def set_ident(val_type, val):

        ident = '{}_{}'.format(val_type, val)
        ident = ident.replace('>', '')
        ident = ident.replace('<', '')
        ident = ident.replace(')', '')
        ident = ident.replace('(', '')
        ident = ident.replace('\,', '')
        ident = ident.replace('\'', '')
        ident = ident.replace('\"', '')
        ident = ident.replace(' ', '_')
        ident = ident.replace('.', '_')
        ident = ident.replace('-', '_')
        ident = ident.replace('__', '_')
        ident = ident.replace('__', '_')
        return str(ident)[:50] # not too big

    def func_wrapper(*args, **kwargs):

        idents = []
        """Building a unique key for this call from all it's meta
        data + its parameters."""

        _module_path = set_ident('module_path', func.__module__)
        _class_class = ''
        _class_name = ''
        _method_class = set_ident('method_class', func.__class__.__name__)
        _method_name = set_ident('method_name', func.__name__)

        vals = []
        """Keep the param values handy."""

        for arg in args:

            if 'object at ' in str(arg):
                """The "object at " value is the method's `self`. The value has
                an instance guid - and we don't want it in our key. Playback
                should return the same value for any instance."""

                _class_name = set_ident('class_name', arg.__class__.__name__)
                _class_class = set_ident('class_class', arg.__class__.__class__)

            else:
                """Use any other parameter in the key."""

                arg_val = slugify(str(arg))
                arg_name = arg.__class__.__name__
                arg_class = arg.__class__.__class__

                idents.append(set_ident('arg_class', arg_class))
                idents.append(set_ident('arg_name', arg_name))
                idents.append(set_ident('arg_val', arg_val))
                vals.append(set_ident(arg_name, arg_val))


        # Use the kwargs in the key
        for key, val in kwargs.items():
            """Use all the kwargs."""
            idents.append('{}_{}'.format(key, val))

        idents.insert(0, _method_name)
        idents.insert(0, _method_class)
        idents.insert(0, _class_name)
        idents.insert(0, _class_class)
        idents.insert(0, _module_path)

        ident_key = '__'.join(idents)

        if acr_remote.run_mode == ApiRecorderController.PLAYBACK:
            """PlayBack mode: try to get the last known value for module.class.func(*args**kwargs)."""

            _recording = acr_remote.get(ident_key)

        else:

            _recording = func(*args, **kwargs)
            """Run the function as normal"""

            if acr_remote.power == ApiRecorderController.POWER_ON:
                """Recording mode: store it."""


                package = {
                    'recording': _recording,
                    'ident_key': ident_key,
                    'vals': vals,
                    'module_path': _module_path,
                    'class_class': _class_class,
                    'class_name': _class_name,
                    'method_class': _method_class,
                    'method_name': _method_name,
                }

                acr_remote.set(ident_key, package)

        return _recording
        """Return value."""

    return func_wrapper


def api_class_recorder(decorator):
    """
    Hook the `api_recorder` decorator onto all methods.

    ***Usage***

    ::

        from ghosts.decorators.api_recorder import api_recorder, api_class_recorder

        @api_class_offline(api_recorder)
        class ApiMarshall(object):
            ...

    """
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                if not attr[:2] == '__':
                    setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate
