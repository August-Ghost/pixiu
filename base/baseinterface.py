# -*- coding: utf-8 -*-
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class BaseInterface:

    def __init__(self):
        self.client = AsyncHTTPClient()
        self.request_params = None

    async def communicate(self,** request_params):
        """
        Communicate with remote server with request_params.
        :param request_params: Query arguments. Please refer to:
        http://www.tornadoweb.org/en/stable/httpclient.html#request-objects
        :return: Response from server. tornado.httpclient.HTTPResponse instance
        """
        self.request_params = request_params
        try:
            response = await self.client.fetch(HTTPRequest(**self.request_params,
                                                           allow_nonstandard_methods=True))
        except Exception as e:
            await self.on_failure(e)
            raise e
        else:
            await self.on_success(response)
            return response


    async def on_success(self, response):
        """
        This method will be called if no error occurred.
        :param response:
        :return:
        """
        pass


    async def on_failure(self, error):
        """
        This method will be called if any error occurred.
        :param error:
        :param response:
        :return:
        """
        raise error