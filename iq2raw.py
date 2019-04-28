#!/usr/bin/python3.5

import numpy as np
from scipy import signal
from scipy.fftpack import fftshift
import matplotlib.pyplot as plt
import sys
from scipy.io import wavfile


def load_iq(filename):
    x = np.fromfile(filename, np.uint8) + np.int8(-127) #adding a signed int8 to an unsigned one results in an int16 array
    return x.astype(np.int8).reshape((x.size//2, 2))    #we cast it back to an int8 array and reshape

def load_iq_complex(filename):
    x = np.fromfile(filename, np.uint8) - np.float32(127.5) #by subtracting a float32 the resulting array will also be float32
    return 8e-3*x.view(np.complex64)                        #viewing it as a complex64 array then yields the correct result

def load_iq_complex_buffer(buffer):
    x = np.frombuffer(buffer, np.uint8) - np.float32(127.5) #by subtracting a float32 the resulting array will also be float32
    return 8e-3*x.view(np.complex64)                        #viewing it as a complex64 array then yields the correct result


def showWelch(sample_rate, iq_samples):
    f, Pxx = signal.welch(iq_samples, sample_rate, detrend=lambda x: x)
    f, Pxx = fftshift(f), fftshift(Pxx)

    plt.semilogy(f/1e3, Pxx)
    plt.xlabel('f [kHz]')
    plt.ylabel('PSD [Power/Hz]')
    plt.grid()

    plt.xticks(np.linspace(-sample_rate/2e3, sample_rate/2e3, 7))
    plt.xlim(-sample_rate/2e3, sample_rate/2e3)
    plt.show()



f = sys.stdin.buffer
f=open("/tmp/sound.dat","rb")
fout=open("/tmp/sound_backup.raw","wb")

while True:
    byte = f.read(-1)
    #byte = f.read(1024)
    if byte==b'':
        #sys.stderr.write("End")
        break

    iq_samples=load_iq_complex_buffer(byte)

    sample_rate = 2400000
    sample_rate_fm = 240000                       #decimate by 10
    audio_rate = 48000

    iq_comercial = signal.decimate(iq_samples, sample_rate//sample_rate_fm)


    angle_comercial = np.unwrap(np.angle(iq_comercial))
    demodulated_comercial = np.diff(angle_comercial)

    audio_comercial = signal.decimate(demodulated_comercial, \
        sample_rate_fm//audio_rate, zero_phase=True)

    audio_comercial = np.int16(1e4*audio_comercial)

    sys.stdout.buffer.write (audio_comercial.tobytes())
    fout.write(audio_comercial.tobytes())

fout.flush()
fout.close()

#showWelch(sample_rate = 2400000,iq_samples=iq_samples)



