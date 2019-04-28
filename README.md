# SDR Lab

## Install
- pip3 install numpy
- pip3 install scipy
- pip3 install matplotlib


## Hear FM radio with rtl_fm:
1. rtl_fm -M wbfm -f 103.1M -g 20 -r 48k /tmp/sound.raw
2. ./raw2wav.py
3. Listen the soundfile "/tmp/sound.wav" with audacity for example



rtl_sdr -f 89000000 -g 20 -s 2400000 -n 24000000 - > ./iq2.dat 

