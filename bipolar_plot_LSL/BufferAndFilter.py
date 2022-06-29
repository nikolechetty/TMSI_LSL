import numpy as np 
import scipy.signal

class processData:

    def __init__(self, nSamples, nChannels, filterAfterN): 
        self.rawData = np.empty(nSamples, nChannels)
        self.filteredData = np.empty(nSamples, nChannels)
        self.filterAfterN = filterAfterN
        self.counter = 0 
        
    # raw data - empty numpy 
    # filtered data - empty numpy 
    # counter 

    def addSample(self, newSample):
    # numpy.roll 
    # FIFO buffer 
    # pop data from the array and push new sample 
        self.rawData = np.roll(self.rawData, -1, axis = 0)
        self.rawData[-1,:] = newSample
        self.counter += 1
        

    def BandpassFilterData(self, lowCutoff, highCutoff, order, samplingRate):
        b, a = scipy.signal.butter(order, [lowCutoff, highCutoff], 'bandpass',fs=samplingRate) #analog=True
        self.filteredData = scipy.signal.filtfilt(b, a, self.rawData, axis = 0)

        
         