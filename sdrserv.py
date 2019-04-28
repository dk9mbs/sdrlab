#!/usr/bin/python3.5

from __future__ import print_function
import subprocess
import sys
import argparse
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import signal
import os


frequency=103100000
samplerate=2400000
gain=20
outputfile='-'


parser = argparse.ArgumentParser(description='Get iq datastream form radio device')

parser.add_argument("-f", "--frequency", dest="frequency",
                        help="Frequency (in Hz)", metavar="FREQUENCY")
parser.add_argument("-o", "--output", dest="outputfile",
                        help="Onput file", metavar="FILE")
parser.add_argument("-s", "--sample-rate", dest="samplerate",
                        help="Samplerate", metavar="SAMPLERATE")
parser.add_argument("-g", "--gain", dest="gain",
                        help="Gain", metavar="GAIN")
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


# TCP Server

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address, file=sys.stderr)
        #client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = "test"
    #name = client.recv(BUFSIZ).decode("utf8")
    #welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    #client.send(bytes(welcome, "utf8"))
    #msg = "%s has joined the chat!" % name
    #broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        try:
            msg = client.recv(BUFSIZ)
            if msg == bytes("{quit}", "utf8"):
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                break
        except:
            del clients[client]
            break
        


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""
    for sock in list(clients): # list is a copy of clients
        try:
            sock.send(msg)
        except:
            del client[sock]
            print("Closed connection by peer!\n", file=sys.stderr)
            
clients = {}
addresses = {}

HOST = ''
PORT = 33001
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

SERVER.listen(5)
print("Waiting for tcp connection...", sys.stderr)
ACCEPT_THREAD = Thread(target=accept_incoming_connections)
ACCEPT_THREAD.start()
# END TCP Server

def handler(signum, frame):
    print('Strg+c', signum)
    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    ACCEPT_THREAD.join()
    SERVER.close()
    sys.exit()

signal.signal(signal.SIGINT, handler)




cmd = 'rtl_sdr -f %s -s %s -g %s %s' % (frequency,samplerate,gain,outputfile)
print('IQ process cmd => %s\n' % cmd, file=sys.stderr)

p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
while True:
    out=p.stdout.read(16384)
    if out=='' and p.poll() != None:
        break
    if out != '':
        broadcast(out)        
        #sys.stdout.buffer.write(out)
        #sys.stdout.flush()

