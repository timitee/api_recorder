# -*- encoding: utf-8 -*-
from ghosts.decorators.api_recorder import api_recorder, api_class_recorder
from ghosts.decorators.tests.scenario import api_response

class ApiMarshall(object):

    @api_recorder
    def decorated_m(self, val):
        return api_response.format(self.__module__, 'ApiMarshall', 'm1', val)


    def undecorated_m(self, val):
        return api_response.format(self.__module__, 'ApiMarshall', 'm2', val)


class BpiMarshall(object):

    @api_recorder
    def decorated_m(self, val):
        return api_response.format(self.__module__, 'BpiMarshall', 'm1', val)


    def undecorated_m(self, val):
        return api_response.format(self.__module__, 'BpiMarshall', 'm2', val)

@api_class_recorder(api_recorder)
class ApiClassDecorated(object):

    def decorated_m(self, val):
        return api_response.format(self.__module__,'ApiClassDecorated', 'm1', val)
