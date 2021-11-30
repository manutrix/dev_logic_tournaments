from . import BaseController
from http_server import Response, Server
from singleton import singleton


@singleton
class Root(BaseController):
    def __init__(self):
        super().__init__()

        self.add_route('get', '/', self.get_root)
        self.add_route('get', '/ping', self.get_ping)

    def get_root(self, request):
        return Response()

    def get_ping(self, request):
        return Response()
