#!/usr/bin/python3.5

from __future__ import print_function

import sys
import argparse
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import signal
import os
from common.streamserver import StreamServer
from hardware.rtlsdr import RtlSdr as Hardware


hwcfg={'frequency': 103100000, 'samplerate': 2400000, 'gain': 20, 'outputfile': '-'}
iqstreamcfg={'host': '0.0.0.0', 'port': 33000}

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
    hwcfg['frequency']=args.frequency

if args.outputfile:
    hwcfg['outputfile']=args.outputfile

if args.samplerate:
    hwcfg['samplerate']=args.samplerate

if args.gain:
    hwcfg['gain']=args.gain

if args.port:
    iqstreamcfg['port']=int(args.port)


iqstream= StreamServer(**iqstreamcfg)
iqstream.start()
print("Waiting for tcp connection...", sys.stderr)


def handler(signum, frame):
    print('Strg+c', signum)
    os.killpg(os.getpgid(hardware.p.pid), signal.SIGTERM)
    iqstream.server.close()
    iqstream.stop()
    iqstream.join()
    sys.exit()

signal.signal(signal.SIGINT, handler)


hardware=Hardware()
hardware.get_iq_stream(iqstream, **hwcfg)
