# -*- encoding: utf-8 -*-
from api_recorder.api_recorder import api_recorder, api_class_recorder

scenario_val = 'ISeeYouGhost!'

def api_response(module_, class_, method_, vals_):
    return {'mod': module_, 'cls': class_, 'mtd': method_, 'val': vals_}

class ApiMarshall(object):

    @api_recorder
    def decorated_m(self, val):
        return api_response(self.__module__,'ApiMarshall', 'decorated_m', val)

    def undecorated_m(self, val):
        return api_response(self.__module__,'ApiMarshall', 'undecorated_m', val)


class BpiMarshall(object):

    @api_recorder
    def decorated_m(self, val):
        return api_response(self.__module__,'BpiMarshall', 'decorated_m', val)

    def undecorated_m(self, val):
        return api_response(self.__module__,'BpiMarshall', 'undecorated_m', val)


#@api_class_recorder(api_recorder)
class ApiSuperClassDecorated(object):

    def decorated_super(self, val):
        return api_response(self.__module__,'ApiSuperClassDecorated', 'decorated_super', val)


#@api_class_recorder(api_recorder)
class ApiSubClassDecorated(ApiSuperClassDecorated):

    def decorated_sub(self, val):
        return api_response(self.__module__,'ApiSubClassDecorated', 'decorated_sub', val)
