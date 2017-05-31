# -*- encoding: utf-8 -*-
from ghosts.api_recorder.api_recorder import api_recorder, api_class_recorder
from ghosts.api_recorder.tests.scenario import api_response

class ApiMarshall(object):

    @api_recorder
    def decorated_m(self, val):
        return api_response(self.__module__, 'ApiMarshall', 'decorated_m', val)


    def undecorated_m(self, val):
        return api_response(self.__module__, 'ApiMarshall', 'undecorated_m', val)


class BpiMarshall(object):

    @api_recorder
    def decorated_m(self, val):
        return api_response(self.__module__, 'BpiMarshall', 'decorated_m', val)


    def undecorated_m(self, val):
        return api_response(self.__module__, 'BpiMarshall', 'undecorated_m', val)

#@api_class_recorder(api_recorder)
class ApiSuperClassDecorated(object):

    def decorated_super(self, val):
        return api_response(self.__module__,'ApiSuperClassDecorated', 'decorated_super', val)


class SuperClass(ApiSuperClassDecorated):

    def decorated_sub(self, val):
        return api_response(self.__module__,'SuperClass', 'decorated_sub', val)
