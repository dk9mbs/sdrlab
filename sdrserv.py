#!/usr/bin/python3.5

from __future__ import print_function
import subprocess
import sys
import argparse
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import signal
import os
from common.streamserver import StreamServer

frequency=103100000
samplerate=2400000
gain=20
outputfile='-'

host = '0.0.0.0'
port = 33000


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
    frequency=args.frequency

if args.outputfile:
    outputfile=args.outputfile

if args.samplerate:
    samplerate=args.samplerate

if args.gain:
    gain=args.gain

if args.port:
    port=int(args.port)


server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
server.listen(5)

iqstream=StreamServer(server)
iqstream.start()
print("Waiting for tcp connection...", sys.stderr)


def handler(signum, frame):
    print('Strg+c', signum)
    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    iqstream.stop()
    iqstream.join()
    server.close()
    sys.exit()

signal.signal(signal.SIGINT, handler)




cmd = 'rtl_sdr -f %s -s %s -g %s %s' % (frequency,samplerate,gain,outputfile)
print('IQ process cmd => %s' % cmd, file=sys.stderr)

p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
while True:
    out=p.stdout.read(16384)
    if out=='' and p.poll() != None:
        break
    if out != '':
        iqstream.broadcast(out)        

