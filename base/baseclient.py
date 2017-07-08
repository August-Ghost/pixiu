# -*- coding: utf-8 -*-
from tornado.httpclient import HTTPError


class ClientError(Exception):
    def __init__(self, *args, **kargs):
        super(ClientError, self).__init__(*kargs.values())


class BaseClient:
    def __init__(self, interface):
        self.interface = interface

    async def query(self, **qurey_kargs):
        """

        :param qurey_kargs: Query arguments for interface. Please refer to:
        http://www.tornadoweb.org/en/stable/httpclient.html#request-objects
        :return: query result. tornado.httpclient.HTTPResponse instance
        """
        try:
            result = await self.interface.communicate(**qurey_kargs)
        except HTTPError as e:
            await self.on_qurey_failed(e)
        else:
            await self.on_query_succeed(result)
            return result

    async def on_query_succeed(self, reply):
        """"
        This method will be called if no error occurred.
        :param response:
        :return:
        """
        pass

    async def on_qurey_failed(self, err):
        """
        This method will be called if any error occurred.
        :param error:
        :param response:
        return:
         """
        pass





