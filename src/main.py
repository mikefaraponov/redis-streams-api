from functools import partial
from http.server import ThreadingHTTPServer
from os import environ
from signal import signal, SIGTERM, SIGINT
from threading import Thread

from redis import Redis

from src.components.ad_events_controller import AdEventsController
from src.components.config import Config
from src.components.listener import Listener
from src.components.suicide import Suicide

if __name__ == '__main__':
    config = Config(environ)
    conn = Redis(host=config.redis_host,
                 port=config.redis_port)
    controller = AdEventsController(conn)
    ListenerWithController = partial(Listener, controller)
    server = ThreadingHTTPServer(config.address, ListenerWithController)
    server_thread = Thread(target=server.serve_forever)
    server_thread.start()
    suicide = Suicide(server, conn)
    signal(SIGTERM, suicide.die)
    signal(SIGINT, suicide.die)
    server_thread.join()
