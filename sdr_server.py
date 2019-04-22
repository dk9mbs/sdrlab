import subprocess
import sys

cmd = "rtl_sdr -f 91509100 -s 240000 -g 20 -"

p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)

while True:
    out=p.stdout.read(4096)
    if out=='' and p.poll() != None:
        sys.stdout.write('End')
        break
    if out != '':
        sys.stdout.write(out)
        sys.stdout.flush()
        
