from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show

class FirFilter:
    def __init__(self):
        self.__window=[]
        self.__window_width=5
        self.__average=0
        self.__taps=[]
        self.__init(100,400)

        for _ in range(0,self.__window_width):
            self.__window.append(0)
            #self.__window[x]=0

    def get_window(self):
        return self.__window

    def get_taps(self):
        return self.__taps

    def add_value(self, value):
        average=0
        for x in range(self.__window_width-1,0,-1):
            self.__window[x]=self.__window[x-1]
            average+=self.__window[x]
        
        self.__window[0]=value 
        average+=value
        self.__average=average/self.__window_width 

    def get_filter_value(self):
        return self.__average


    def __init(self,sample_rate):
        #------------------------------------------------
        # Create a signal for demonstration.
        #------------------------------------------------

        #sample_rate = 100.0
        #nsamples = 400
        #t = arange(nsamples) / sample_rate
        #x = cos(2*pi*0.5*t) + 0.2*sin(2*pi*2.5*t+0.1) + \
        #        0.2*sin(2*pi*15.3*t) + 0.1*sin(2*pi*16.7*t + 0.1) + \
        #            0.1*sin(2*pi*23.45*t+.8)


        #------------------------------------------------
        # Create a FIR filter and apply it to x.
        #------------------------------------------------

        # The Nyquist rate of the signal.
        nyq_rate = sample_rate / 2.0

        # The desired width of the transition from pass to stop,
        # relative to the Nyquist rate.  We'll design the filter
        # with a 5 Hz transition width.
        width = 5.0/nyq_rate

        # The desired attenuation in the stop band, in dB.
        ripple_db = 60.0

        # Compute the order and Kaiser parameter for the FIR filter.
        N, beta = kaiserord(ripple_db, width)

        # The cutoff frequency of the filter.
        cutoff_hz = 10.0

        # Use firwin with a Kaiser window to create a lowpass FIR filter.
        taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

        self.__taps=taps
        # Use lfilter to filter x with the FIR filter.
        #filtered_x = lfilter(taps, 1.0, x)





if __name__ == "__main__":
    filter=FirFilter()
    print(filter.get_window())

    for x in range(1,6):
        filter.add_value(x)
        print('x=>%s value=>%s filter=>%s' % (x,filter.get_filter_value(), filter.get_window()))
        

    print(filter.get_window())
    #print(filter.get_filter_value())

