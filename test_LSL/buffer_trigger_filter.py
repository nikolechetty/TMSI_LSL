from statistics import mean
from tkinter import NS
import numpy as np 
import scipy.signal


class processData:

    def __init__(self, nChannels, samplingRate, nSamples, filterAfterN): 
        self.nSamples = nSamples
        print('Length of buffer set to:', nSamples)
        self.nChannels = nChannels
        print('Channels to record:', nChannels)
        self.filterAfterN = filterAfterN
        self.samplingRate = samplingRate

        self.rawData = np.empty((self.nSamples, self.nChannels))
        self.bpFilteredData = np.empty((self.nSamples, self.nChannels))
        self.lpFilteredData = np.empty((self.nSamples, self.nChannels))
        self.rectifiedData = np.empty((self.nSamples, self.nChannels))
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


    def bandpassFilterData(self, bpLowCutoff, bpHighCutoff, order):
        b, a = scipy.signal.butter(order, [bpLowCutoff, bpHighCutoff], 'bandpass',fs=self.samplingRate)
        self.bpFilteredData = scipy.signal.filtfilt(b, a, self.rawData, axis = 0)

    def rectifyData(self):
        self.rectifiedData = abs(self.bpFilteredData)

    def lowpassFilterData(self, lpHIghCutoff, order):
        b, a = scipy.signal.butter(order, lpHIghCutoff, 'lowpass',fs=self.samplingRate) 
        self.lpFilteredData = scipy.signal.filtfilt(b, a, self.rectifiedData, axis = 0)

    def takeMean(self):
        self.meanData = np.mean(self.lpFilteredData)

    def processBuffer(self, bpLowCutoff, bpHighCutoff, lpHIghCutoff, order):
        self.bandpassFilterData(bpLowCutoff, bpHighCutoff, order)
        self.rectifyData()
        self.lowpassFilterData(lpHIghCutoff, order)
        self.takeMean()




