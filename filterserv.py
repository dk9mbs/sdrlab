#!/usr/bin/python3.5

from __future__ import print_function

import sys
import json
import time
import argparse
import os
import signal

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
from dk9mbs.common.streamserver import StreamServer
from dk9mbs.hardware.rtlsdr import RtlSdr as Hardware

from flask import Flask
from flask import render_template
from flask import request
from flask import abort

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler


cfg= {'httpcfg': {'host': '0.0.0.0', 'port': '8081'}}

app = Flask(__name__, template_folder='htdocs/filterserv', static_url_path='/htdocs/filterserv')
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

app.debug=False
app.host=cfg['httpcfg']['host']
app.port=cfg['httpcfg']['port']
app.threaded=True


@app.route('/api/v1.0/auth/login', methods=['POST'])
def login():
    return "OK"





server = WSGIServer((cfg['httpcfg']['host'], int(cfg['httpcfg']['port'])), app, handler_class=WebSocketHandler)
server.serve_forever()
