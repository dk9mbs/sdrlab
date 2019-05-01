import sys
import subprocess

class RtlSdr:
    def __init__(self):
        self.p=None
        
    def get_iq_stream(self, iqstream, **config):
        cmd = 'rtl_sdr -f %s -s %s -g %s %s' % (config['frequency'],config['samplerate'],config['gain'],config['outputfile'])
        print('IQ process cmd => %s' % cmd, file=sys.stderr)

        self.p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        while True:
            out=self.p.stdout.read(16384)
            if out=='' and self.p.poll() != None:
                break
            if out != '':
                iqstream.write(out)

