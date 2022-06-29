from tkinter import NS
import numpy as np 
import scipy.signal


class processData:

    def __init__(self, nChannels, samplingRate, nSamples, filterAfterN, bpLowCutoff, bpHighCutoff, order): 
        self.nSamples = nSamples
        print('Length of buffer set to:', nSamples)
        self.nChannels = nChannels
        print('Channels to record:', nChannels)
        self.filterAfterN = filterAfterN
        print('Data will be filted every', filterAfterN, 'samples')

        self.bpLowCutoff = bpLowCutoff
        self.bpHighCutoff = bpHighCutoff
        self.order = order
        self.samplingRate = samplingRate

        self.rawData = np.empty((self.nSamples, self.nChannels))
        self.bpFilteredData = np.empty((self.nSamples, self.nChannels))
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

        if self.counter % self.filterAfterN == 1:
            self.bandpassFilterData()


    def bandpassFilterData(self):
        b, a = scipy.signal.butter(self.order, [self.bpLowCutoff, self.bpHighCutoff], 'bandpass',fs=self.samplingRate) #analog=True
        self.bpFilteredData = scipy.signal.filtfilt(b, a, self.rawData, axis = 0)

        
         