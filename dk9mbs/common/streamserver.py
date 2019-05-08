#!/usr/bin/python3.5

from __future__ import print_function
import subprocess
import sys
import argparse
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import signal
import os


class StreamServer(Thread):
    def __init__(self,logger, **config):
        Thread.__init__(self)
        self.config=config
        self.logger=logger
        self.clients={}
        self.addresses={}
        #self.server=server
        self.bufsiz = 1024

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((config['host'], config['port']))
        self.server.listen(5)
    

    def run(self):
        ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        ACCEPT_THREAD.start()

    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            client, client_address = self.server.accept()
            print("%s:%s has connected." % client_address, file=self.logger)
            #client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()


    def handle_client(self,client):  # Takes client socket as argument.
        """Handles a single client connection."""
        name = "test"
        #name = client.recv(BUFSIZ).decode("utf8")
        #welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        #client.send(bytes(welcome, "utf8"))
        #msg = "%s has joined the chat!" % name
        #broadcast(bytes(msg, "utf8"))
        self.clients[client] = name

        while True:
            try:
                msg = client.recv(self.bufsiz)
                if msg == bytes("{quit}", "utf8"):
                    client.send(bytes("{quit}", "utf8"))
                    client.close()
                    del self.clients[client]
                    break
            except:
                del self.clients[client]
                break


    def write(self,msg, prefix=""):
        """Broadcasts a message to all the clients."""
        for sock in list(self.clients): # list is a copy of clients
            try:
                sock.send(msg)
            except:
                del self.clients[sock]
                print("Closed connection by peer!", file=self.logger)


# END TCP Server
