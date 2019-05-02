import sys
import subprocess
import os
import signal
from threading import Thread, Lock
import time

class RtlSdr(Thread):
    def __init__(self,logger, iqstream, **config):
        Thread.__init__(self)
        self.p=None
        self.iqstream=iqstream
        self.config=config
        self.logger=logger
        self.__init=True 
        
    def run(self):
                
        while True:
            if self.__init:
                bufsiz=int(self.config['output_block_size'])
                cmd = 'rtl_sdr -b %s -f %s -s %s -g %s %s' % (bufsiz, self.config['frequency']
                                                              ,self.config['samplerate']
                                                              ,self.config['gain']
                                                              ,self.config['outputfile'])
                print('IQ process cmd => %s' % cmd, file=self.logger)

                self.p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
                self.__init=False

            out=self.p.stdout.read(bufsiz)
            #if out=='' and self.p.poll() != None:
            #    break
            if out != '' and self.__init==False:
                self.iqstream.write(out)


    def reinit(self, **config):
        self.__init=True
        self.config=config
        self.p.stdout=None
        self.p.stderr=None
        os.killpg(os.getpgid(self.p.pid), signal.SIGTERM)
