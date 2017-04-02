# -*- encoding: utf-8 -*-
"""Record/Playback an api method's return values.

TODO: Make @api_automock decorator separate.
"""
import collections
import hashlib
from slugify import slugify
from ghosts.api_recorder.api_controller import ApiRecorderController

acr_remote = ApiRecorderController('pyghosts', 'root', False)

def dlistyfy(this_list):
    """Return a list as a settable list of strings."""

    arg_name = this_list.__class__.__name__

    if this_list:

        try:

            this_list = sorted(this_list)

            _dlistyfy = set_ident('dlistyfy_{}'.format(arg_name), '_'.join(this_list))
            """The sorted list as a key."""

            return set([_dlistyfy])

        except Exception as ex:
            """Sorting a List of Dicts error."""

            if len(this_list) > 0:

                ddictions = set(['ddiction'])
                for poss_dict in this_list:
                    if isinstance(poss_dict, dict):
                        ddictions.union(ddiction(poss_dict, arg_name))
                return ddictions

            else:
                return set([set_ident('dlistyfy_{}'.format(arg_name), 'blank')])

    """Return a placeholder for the arg."""
    return set([set_ident('dlistyfy_{}'.format(arg_name), 'blank')])


def ddiction(this_dictionary, arg_name):
    ddictions = set(['ddiction'])
    for k, v in this_dictionary.items():
        zub_key_ident = set_ident('{}_{}'.format(arg_name, k), v)
        ddictions.add(zub_key_ident)
    return ddictions


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
    return str(ident) #[:80] # not too big - hashing... big as you like.


def api_recorder(func):
    """Record/Playback a method output keyed to input."""

    def func_wrapper(*args, **kwargs):

        if acr_remote.power == ApiRecorderController.POWER_OFF:
            """Recording mode off: return it."""
            return func(*args, **kwargs)
            """Run the function as normal"""

        clues = set(['1clueset1'])
        """Building a unique key for this call from all it's meta
        data + its parameters."""

        module_path_ = set_ident('module_path', func.__module__)
        class_class_ = '' #get later but put in this order
        class_name_ = '' #get later but put in this order
        method_class_ = set_ident('method_class', func.__class__.__name__)
        method_name_ = set_ident('method_name', func.__name__)

        _vals = set(['2valsset2'])

        """Keep the param values handy and add to the meta."""

        for arg in args:

            if isinstance(arg, list):

                list_set = dlistyfy(arg)
                clues = clues.union(list_set)

                _vals = _vals.union(list_set)
                """Keep in handy as val."""


            elif isinstance(arg, dict):


                dict_set = ddiction(arg, 'dict')
                clues = clues.union(dict_set)

                _vals = _vals.union(dict_set)
                """Keep in handy as val."""


            elif 'object at ' in str(arg):
                """Important: Playback should return the same value for any
                instance. The "object at " value is the method's `self`. The
                value has an instance guid - and we don't want it in our key.
                """

                class_name_ = set_ident('class_name', arg.__class__.__name__)
                class_class_ = set_ident('class_class', arg.__class__.__class__)

            else:

                """Use any other parameter in the key."""

                arg_val = slugify(str(arg))
                arg_name = arg.__class__.__name__
                arg_class = arg.__class__.__class__

                vclass = set_ident('arg_class', arg_class)
                vname = set_ident('arg_name', arg_name)
                vval = set_ident('arg_val', arg_val)

                clues.add('{}_{}_{}'.format(vclass, vname, vval))

                _vals.add(set_ident(arg_name, arg_val))
                """Keep in handy as val."""


        # Use the kwargs in the key
        for key, val in kwargs.items():

            if isinstance(val, list):

                list_as_set = dlistyfy(val)

                clues = clues.union(list_as_set)

            elif isinstance(val, dict):

                dict_as_set = ddiction(val, 'kwargdict')

                clues = clues.union(dict_as_set)

            else:
                """Use all the kwargs."""

                zwarg = set_ident('kwarg_{}'.format(key), val)
                clues.add(zwarg)

                _vals.add(zwarg)
                """Keep in handy as val."""



        if clues:
            clues = sorted(clues)
        if _vals:
            _vals = sorted(_vals)

        # Put in order of ancestors.
        clues.insert(0, method_name_)
        clues.insert(0, method_class_)
        clues.insert(0, class_name_)
        clues.insert(0, class_class_)
        clues.insert(0, module_path_)

        call_sig = '__'.join(clues)
        #_key_hex = call_sig.hexdigest()
        _key_md5 = hashlib.md5(call_sig.encode())
        _key_md5_hex = _key_md5.hexdigest()

        call_incre = acr_remote.acr_counter.incr(_key_md5_hex)
        _incre_hex = '{}__{}'.format(call_sig, call_incre)
        _incre_md5 = hashlib.md5(_incre_hex.encode())
        _incre_md5_hex = _incre_md5.hexdigest()

        _call_md5 = hashlib.md5(
                            _incre_md5_hex.encode()
                            ) # or: _key_md5_hex
        """Change what you want to hash here."""

        call_signature_key = _call_md5.hexdigest()

        print(method_name_, ':', call_signature_key)

        package = {
            'recording': None,
            'call_sig': call_sig,
            'call_incre': call_incre,
            'call_sig': call_signature_key,
            'vals': [] if not _vals else list(_vals),
            'module_path': module_path_,
            'class_class': class_class_,
            'class_name': class_name_,
            'method_class': method_class_,
            'method_name': method_name_,
        }

        if acr_remote.run_mode == ApiRecorderController.PLAYBACK:
            """PlayBack mode: try to get the last known value for module.class.func(*args**kwargs)."""

            # acr_remote.build_mock_if_safe(call_signature_key, package)
            
            _recording = acr_remote.get(call_signature_key)

        else:
            """Recording."""

            _recording = func(*args, **kwargs)
            """Run the function as normal"""

            package['recording'] = _recording

            acr_remote.set(call_signature_key, package)

        return _recording
        """Return value."""

    return func_wrapper


def api_class_recorder(decorator):
    """
    Hook the `api_recorder` decorator onto all methods.

    ***Usage***

    ::

        from ghosts.api_recorder.api_recorder import api_recorder, api_class_recorder

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
