from http_server import Response, Server


class BaseController:
    def __init__(self):
        self.routes = {
            'get': [],
            'post': [],
            'put': [],
            'patch': [],
            'delete': []
        }

    def add_route(self, verb, pattern, method):
        route = {
            'pattern': pattern.lower(),
            'method': method
        }

        self.routes[verb.lower()].append(route)
