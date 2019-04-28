#!/usr/bin/python3.5

import subprocess
import sys

#cmd = "rtl_sdr -f 89000000 -s 2400000 -g 0 -"
cmd = "rtl_sdr -f 103100000 -s 2400000 -g 10 -"

p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)

while True:
    out=p.stdout.read(4096)
    if out=='' and p.poll() != None:
        break
    if out != '':
        sys.stdout.buffer.write(out)
        sys.stdout.flush()

