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
        self.__run=False 
        
    def run(self):
        while True:
            if not self.__run:
                bufsiz=int(self.config['output_block_size'])

                cmd = 'rtl_sdr -b {output_block_size} -f {frequency} -s {samplerate} -g {gain} {outputfile}'
                
                print('IQ process template => %s' % cmd, file=self.logger)

                for argument in self.config:
                    print ('{%s} => %s' % (argument,str(self.config[argument])), file=self.logger)
                    cmd=cmd.replace('{%s}' % argument , str(self.config[argument]))
                
                print('IQ process cmd => %s' % cmd, file=self.logger)

                self.p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
                self.__run=True
            
            out=self.p.stdout.read(bufsiz)
            # Do notsend any eof symbols.
            # So the client doesn't disconnect from the server
            #if out=='' and self.p.poll() != None:
            #    break
            if out != '':
                self.iqstream.write(out)


    def update(self, **config):
        for argument in config:
            self.config[argument]=config[argument]
        
        self.__run=False
        self.p.stdout=None
        self.p.stderr=None
        os.killpg(os.getpgid(self.p.pid), signal.SIGTERM)
