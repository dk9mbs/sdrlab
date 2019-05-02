# SDR Lab

## Install
- pip3 install numpy
- pip3 install scipy
- pip3 install matplotlib
- pip3 install Flask
- pip3 install bottle

## Hear FM radio with rtl_fm
1. rtl_fm -M wbfm -f 103.1M -g 20 -r 48k /tmp/sound.raw
2. ./raw2wav.py
3. Listen the soundfile "/tmp/sound.wav" with audacity for example

## Capture IQ data with rtl_sdr (command for sdrserv.py)
rtl_sdr -f 89000000 -g 20 -s 2400000 -n 24000000 - > ./iq2.dat 

## sdrlab tcp server for captering ig data over the network
./sdrserv.py -f 89000000 -g 10 -o - -s 2400000 -p 33005

