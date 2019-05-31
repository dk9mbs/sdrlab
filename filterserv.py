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
from dk9mbs.signal.firfilter import FirFilter as Filter

from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import make_response

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

import io
import base64
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_svg import FigureCanvasSVG as FigureCanvas


cfg= {'httpcfg': {'host': '0.0.0.0', 'port': '8081'}}

app = Flask(__name__, template_folder='htdocs/filterserv', static_url_path='/htdocs/filterserv')
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

app.debug=False
app.host=cfg['httpcfg']['host']
app.port=cfg['httpcfg']['port']
app.threaded=True



def build_graph():
    sample_rate = 1000.0
    f=50.0
 
    t =  np.arange(1, step=1/sample_rate) 
    samples = np.sin(2*np.pi*f*t) + 1*np.sin(2*np.pi*(2*f)*t) +\
        1*np.sin(2*np.pi*4*f*t) 

    samples = np.sin(2*np.pi*f*1*t) + 0.2*np.sin(2*np.pi*f*2.5*t+0.1) + \
            0.2*np.sin(2*np.pi*f*15.3*t) + 0.1*np.sin(2*np.pi*f*16.7*t + 0.1) + \
                0.1*np.sin(2*np.pi*f*23.45*t+.8)+0.1*np.sin(2*np.pi*f*8*t)


    #for n in range(len(samples)):
    #    samples[n]=0
    #samples[0]=1



    fft_in=np.fft.fft(samples)
    n_in=int(len(fft_in)/2+1)

    filter=Filter(sample_rate,50.0,10.0,500)

    out=[]
    for x in samples:
        filter.add_value(x)
        out.append(filter.get_filter_value())


    fft=np.fft.fft(out)
    n=int(len(fft)/2+1)


    #fig=plt.figure(1)
    fig=plt.figure(figsize=(9, 9))
    plt.clf()

    ax1=fig.add_subplot(221)
    ax1.plot(samples)
    ax1.grid(True)
    ax1.set_ylabel('Amplitude')
    ax1.set_xlabel('t in samples')
    ax1.set_title('in')
 
    ax2=fig.add_subplot(222)
    ax2.plot(np.abs(fft_in[:n] ))
    ax2.grid(True)
    ax2.set_ylabel('Amplitude')
    ax2.set_xlabel('t in samples')
    ax2.set_title('fft in')

    ax3=fig.add_subplot(223)
    ax3.plot(out)
    ax3.grid(True)
    ax3.set_ylabel('Amplitude')
    ax3.set_xlabel('t in samples')
    ax3.set_title('out')

    ax4=fig.add_subplot(224)
    ax4.plot(np.abs(fft[:n] ))
    ax4.grid(True)
    ax4.set_ylabel('Amplitude')
    ax4.set_xlabel('t in samples')
    ax4.set_title('fft out')

    img = io.BytesIO()
    plt.savefig(img, format='svg')
    img.seek(0)
    response=make_response(img.getvalue())
    response.headers['Content-Type'] = 'image/scg+xml'
    return response


@app.route('/', methods=['GET'])
def index():
    return render_template('index.htm')

@app.route('/diagram.svg', methods=['GET'])
def get_diagram():
    return build_graph()

server = WSGIServer((cfg['httpcfg']['host'], int(cfg['httpcfg']['port'])), app, handler_class=WebSocketHandler)
server.serve_forever()
