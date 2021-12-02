import json, re
from singleton import singleton
from http.server import BaseHTTPRequestHandler, HTTPServer


@singleton
class Server(HTTPServer):
    controllers = []

    def __init__(self, port=8080):
        super().__init__(('', port), ServerHandler)
        pass

    def start(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        self.server_close()

        return self

    def register_controller(self, controller):
        self.controllers.append(controller)


class ServerHandler(BaseHTTPRequestHandler):
    def _generate_headers(self, response):
        self.send_response(response.code, response.message)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _execute_controller(self, response):
        request = Request(self)

        if request.controller_route is not None:
            response = request.controller_route['method'](request)

        self._generate_headers(response)
        if response.body:
            self.wfile.write(json.dumps(response.body).encode())

    def do_GET(self):
        self._execute_controller(self._get_default_response(404))

    def do_POST(self):
        self._execute_controller(self._get_default_response(501))

    def do_PUT(self):
        self._execute_controller(self._get_default_response(501))

    def do_PATCH(self):
        self._execute_controller(self._get_default_response(501))

    def do_DELETE(self):
        self._execute_controller(self._get_default_response(501))

    def _get_default_response(self, code):
        if code == 404:
            return Response(404, 'Not Found')
        elif code == 501:
            return Response(501, 'Not Implemented')

    # def do_POST(self):
    # content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
    # post_data = self.rfile.read(content_length)  # <--- Gets the data itself
    # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
    #              str(self.path), str(self.headers), post_data.decode('utf-8'))
    #
    # self.send_response(200, 'OK')
    # self.send_header('Content-type', 'text/html')
    # self.end_headers()
    # self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
    # pass


class Response:
    def __init__(self, code=200, message='OK', body=None):
        self.code = code
        self.message = message
        self.body = body


class Request:
    def __init__(self, handler):
        self.handler = handler
        self.uri = handler.path

        self.fragments = self._get_fragments()
        self.query_params = self._get_query_params()
        # self.headers = self._get_headers()
        # self.body = self._get_body()

        self.controller_route = self._get_controller_route()
        pass

    def _get_controller_route(self):
        for controller in Server().controllers:
            if self.handler.command.lower() in controller().routes:
                for route in controller().routes[self.handler.command.lower()]:
                    if re.search(route['pattern'] + '($|\?)', self.uri, re.IGNORECASE):
                        return route
        return None

    def _get_fragments(self):
        # Remove query parameters
        uri = self.uri.split('?')[0]

        # Split and remove empty items
        uri_fragments = list(filter(lambda x: (x != ""), uri.split('/')))

        fragments = {}

        for i in range(len(uri_fragments)):
            if i % 2 == 0:
                fragments[uri_fragments[i]] = None

                if len(uri_fragments) > i + 1:
                    fragments[uri_fragments[i]] = uri_fragments[i + 1]

        return fragments

    def _get_query_params(self):
        uri_sections = self.uri.split('?')
        # Todo Make it work even if there is a "?" in the query parameters
        if len(uri_sections) == 1:
            return {}

        uri_query_params = uri_sections[1]

        # Split and remove empty items
        uri_query_params = list(filter(lambda x: (x != ""), uri_query_params.split('&')))

        query_params = list()

        for key_value in uri_query_params:
            key_value = key_value.split('=')

            query_params_item = {
                'key': key_value[0],
                'value': None
            }

            if len(key_value) == 2:
                query_params_item['value'] = key_value[1]

            query_params.append(query_params_item)

        return query_params

    # def _get_headers(self):
    #     return {}
    #
    # def _get_body(self):
    #     return {}
