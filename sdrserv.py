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


hardware=None
iqstream=None

cfg={'iqstreamcfg': {'host': '0.0.0.0', 'port': 33003},
     'hwcfg': {'output_block_size': 16384, 'frequency': 103100000
            , 'samplerate': 2400000, 'gain': 20, 'outputfile': '-'},
     'httpcfg': {'host': '0.0.0.0', 'port': '8080'}
     }

parser = argparse.ArgumentParser(description='Get iq datastream form radio device')

parser.add_argument("-f", "--frequency", dest="frequency",
                        help="Frequency (in Hz)", metavar="FREQUENCY")
parser.add_argument("-o", "--output", dest="outputfile",
                        help="Onput file", metavar="FILE")
parser.add_argument("-s", "--sample-rate", dest="samplerate",
                        help="Samplerate", metavar="SAMPLERATE")
parser.add_argument("-g", "--gain", dest="gain",
                        help="Gain", metavar="GAIN")
parser.add_argument("-p", "--port", dest="port",
                        help="TCP port for listening iq stream", metavar="PORT")
parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose", default=True,
                        help="don't print status messages to stdout")

args = parser.parse_args()
if args.frequency:
    cfg['hwcfg']['frequency']=args.frequency

if args.outputfile:
    cfg['hwcfg']['outputfile']=args.outputfile

if args.samplerate:
    cfg['hwcfg']['samplerate']=args.samplerate

if args.gain:
    cfg['hwcfg']['gain']=args.gain

if args.port:
    cfg['iqstreamcfg']['port']=int(args.port)

print(cfg['iqstreamcfg'], file=sys.stderr)
print(cfg['hwcfg'], file=sys.stderr)

iqstream= StreamServer(sys.stderr, **(cfg['iqstreamcfg']))
iqstream.start()
print("Waiting for tcp connection...", sys.stderr)


def handler(signum, frame):
    pass

def handler_int(signum, frame):
    print('Strg+c', signum)
    iqstream.server.close()
    iqstream.join()
    #server.stop()
    sys.exit()

signal.signal(signal.SIGINT, handler_int)
signal.signal(signal.SIGTERM, handler)

hardware=Hardware(sys.stderr, iqstream, **(cfg['hwcfg']))
hardware.start()

# Flask
from multiprocessing import Process

app = Flask(__name__, template_folder='htdocs')
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

app.debug=False
app.host=cfg['httpcfg']['host']
app.port=cfg['httpcfg']['port']
app.threaded=True

@app.route('/')
def index():
    return render_template('index.htm', config=cfg)

# Websocket
connections = set()
opts = {}

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    connections.add(wsock)

    # Send center frequency and span
    wsock.send(json.dumps(opts))

    while True:
        try:
            wsock.receive()
        except WebSocketError:
            break
    connections.remove(wsock)


# Api v1.0
@app.route('/api/v1.0/config/<scope>', methods=['POST'])
def set_config(scope):
    print("Set config ...")
    if scope=='hardware':
        for key in request.json:
            print('%s => %s' % (key, key))
        hardware.update(**request.json)
    return "OK"

@app.route('/api/v1.0/config/<scope>', methods=['GET'])
def get_config(scope):
    if scope=='hardware':
        return json.dumps(hardware.config)

    if scope=='stream':
        return json.dumps(iqstream.config)

    return json.dumps({'error': 'No config'})

app.run(port=int(cfg['httpcfg']['port']), host=cfg['httpcfg']['host'])

#server = WSGIServer((cfg['httpcfg']['host'], cfg['httpcfg']['port']), app, handler_class=WebSocketHandler)
#try:
#    server.serve_forever()
#except Exception:
#    sys.exit(0)

#server = Process(target=app.run)
#server.start()





