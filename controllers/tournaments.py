from . import BaseController
from http_server import Response
from singleton import singleton


@singleton
class Tournaments(BaseController):
    def __init__(self):
        super().__init__()

        self.add_route('get', '/tournaments', self.get_list)
        self.add_route('get', '/tournaments/[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}', self.get_one)

    def get_list(self, request):
        response = Response()
        response.body = [
            {"key1": "value1", "key2": "value2"},
            {"key1": "value1", "key2": "value2"},
            {"key1": "value1", "key2": "value2"}
        ]

        return response

    def get_one(self, request):
        response = Response()
        response.body = {"key1": "value1", "key2": "value2"}
        return response
