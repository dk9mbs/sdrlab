import sys
import subprocess
import os
import signal
from threading import Thread, Lock

class RtlSdr(Thread):
    def __init__(self,logger, iqstream, **config):
        Thread.__init__(self)
        self.p=None
        self.iqstream=iqstream
        self.config=config
        self.logger=logger
        self.__run=True
        
    def run(self):
        bufsiz=int(self.config['output_block_size'])
        cmd = 'rtl_sdr -b %s -f %s -s %s -g %s %s' % (bufsiz, self.config['frequency']
                                                      ,self.config['samplerate']
                                                      ,self.config['gain']
                                                      ,self.config['outputfile'])
        print('IQ process cmd => %s' % cmd, file=self.logger)

        self.p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        while self.__run:
            out=self.p.stdout.read(bufsiz)
            if out=='' and self.p.poll() != None:
                break
            if out != '':
                self.iqstream.write(out)


    def test(self):
        self.__run=False
        os.killpg(os.getpgid(self.p.pid), signal.SIGTERM)
