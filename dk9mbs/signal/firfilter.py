import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import sys

def plot_response(fs, taps, title):
    w, h = signal.freqz(taps, [1], worN=2000)
    plt.figure()
    plt.plot(0.5*fs*w/np.pi, 20*np.log10(np.abs(h)))
    plt.ylim(-40, 5)
    plt.xlim(0, 0.5*fs)
    plt.grid(True)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain (dB)')
    plt.title(title)
    plt.show()


class FirFilter:
    """  Fir filter
    fs = 44100.0       # Sample rate, Hz
    cutoff = 5000.0    # Desired cutoff frequency, Hz
    trans_width = 250  # Width of transition from pass band to stop band, Hz
    numtaps = 125      # Size of the FIR filter.
    """
    def __init__(self, fs, cutoff, trans_width, numtaps):
        self.__window=[]
        self.__average=0
        self.__taps=[]

        self.__fs=fs
        self.__cutoff=cutoff
        self.__trans_width=trans_width
        self.__num_taps=numtaps

        self.__init_taps(fs, cutoff, trans_width, numtaps)

        for _ in range(0,self.__num_taps):
            self.__window.append(0)

    def get_window(self):
        """ Get the current fir filter window as array """
        return self.__window

    def get_taps(self):
        return self.__taps

    def get_filter_value(self):
        return self.__average

    def add_value(self, value):
        average=0
        for x in range(self.__num_taps-1,0,-1):
            self.__window[x]=self.__window[x-1]
            average+=self.__window[x]*self.__taps[x]
        
        self.__window[0]=value 
        average+=value*self.__taps[0]

        self.__average=average/self.__num_taps 
        print(self.__average)


    def __init_taps(self,fs, cutoff, trans_width, numtaps):

        self.__taps = signal.remez(numtaps, [0, cutoff, cutoff + trans_width, 0.5*fs],[1, 0], Hz=fs)





if __name__ == "__main__":
    sample_rate = 100.0
    nsamples = 100
    f=20.0
 
    t =  np.arange(nsamples, step=0.2) / sample_rate
    samples = np.sin(2*np.pi*f*t) 

    plt.xlabel('Angle [rad]')
    plt.ylabel('Amplitude')

    fft=np.fft.fft(samples)
    n=int(len(fft)/2+1)

    filter=FirFilter(sample_rate,5.0,1.0,10)

    out=[]
    for x in samples:
        filter.add_value(x)
        out.append(filter.get_filter_value())


    fft=np.fft.fft(out)
    n=int(len(fft)/2+1)
    #plt.plot( np.abs(fft[:n]  ))
    plt.plot(out)
    plt.show()
       
    #print(filter.get_window() )

    #plt.figure()
    #plt.grid(True)
    #plt.plot(filter.get_taps(),'bo-', linewidth=2)
    #plt.show()
