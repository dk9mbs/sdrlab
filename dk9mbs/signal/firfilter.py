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
        # lowpass:
        #self.__taps = signal.remez(numtaps, [0, cutoff, cutoff + trans_width, 0.5*fs],[1, 0], Hz=fs)
        
        #highpass:
        #self.__taps = signal.remez(numtaps, [0, cutoff - trans_width, cutoff, 0.5*fs],[0, 1], Hz=fs)

        # bandpass
        #band=[190, 210]
        #edges = [0, band[0] - trans_width, band[0], band[1],band[1] + trans_width, 0.5*fs]
        #self.__taps = signal.remez(numtaps, edges, [0, 1, 0], Hz=fs)

        # bandstop
        band=[50, 240]
        edges = [0, band[0] - trans_width, band[0], band[1], band[1] + trans_width, 0.5*fs]
        self.__taps = signal.remez(numtaps, edges, [1, 0, 1], Hz=fs)



if __name__ == "__main__":
    sample_rate = 1000.0
    f=50.0
 
    t =  np.arange(1, step=1/sample_rate) 
    samples = np.sin(2*np.pi*f*t) + 1*np.sin(2*np.pi*(2*f)*t) +\
        1*np.sin(2*np.pi*4*f*t) 

    samples = np.sin(2*np.pi*f*1*t) + 0.2*np.sin(2*np.pi*f*2.5*t+0.1) + \
            0.2*np.sin(2*np.pi*f*15.3*t) + 0.1*np.sin(2*np.pi*f*16.7*t + 0.1) + \
                0.1*np.sin(2*np.pi*f*23.45*t+.8)+0.1*np.sin(2*np.pi*f*8*t)


    #for n in range(len(samples)):
    #    samples[n]=0
    #samples[0]=1



    fft_in=np.fft.fft(samples)
    n_in=int(len(fft_in)/2+1)

    filter=FirFilter(sample_rate,300.0,10.0,500)

    out=[]
    for x in samples:
        filter.add_value(x)
        out.append(filter.get_filter_value())


    fft=np.fft.fft(out)
    n=int(len(fft)/2+1)


    fig=plt.figure(1)
    plt.clf()

    ax1=fig.add_subplot(221)
    ax1.plot(samples)
    ax1.grid(True)
    ax1.set_ylabel('Amplitude')
    ax1.set_xlabel('t in samples')
    ax1.set_title('in')
 
    ax2=fig.add_subplot(222)
    ax2.plot(np.abs(fft_in[:n] ))
    ax2.grid(True)
    ax2.set_ylabel('Amplitude')
    ax2.set_xlabel('t in samples')
    ax2.set_title('fft in')

    ax3=fig.add_subplot(223)
    ax3.plot(out)
    ax3.grid(True)
    ax3.set_ylabel('Amplitude')
    ax3.set_xlabel('t in samples')
    ax3.set_title('out')

    ax4=fig.add_subplot(224)
    ax4.plot(np.abs(fft[:n] ))
    ax4.grid(True)
    ax4.set_ylabel('Amplitude')
    ax4.set_xlabel('t in samples')
    ax4.set_title('fft out')

    plt.show()

   
