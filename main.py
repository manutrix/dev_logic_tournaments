#!/usr/bin/env python3
from http_server import Server

from controllers.root import Root
from controllers.tournaments import Tournaments
from controllers.subscriptions import Subscriptions
from controllers.games import Games

if __name__ == '__main__':
    s = Server()

    s.register_controller(Root)
    s.register_controller(Tournaments)
    s.register_controller(Subscriptions)
    s.register_controller(Games)

    s.start()
