from statistics import mean
from tkinter import NS
import numpy as np 
import scipy.signal


class processData:

    def __init__(self, nChannels, samplingRate, nSamples, filterAfterN, largeInitializedSpace = 1000000): 
        self.nSamples = nSamples
        print('Length of buffer set to:', nSamples)
        self.nChannels = nChannels
        print('Channels to record:', nChannels)
        self.filterAfterN = filterAfterN
        self.samplingRate = samplingRate

        self.largeInitializedSpace = largeInitializedSpace #### this is arbitary 
        self.rawData = np.empty((self.largeInitializedSpace, self.nChannels))
        self.rawDataBuffer = np.empty((self.nSamples, self.nChannels))
        self.bpFilteredData = np.empty((self.nSamples, self.nChannels))
        self.lpFilteredData = np.empty((self.nSamples, self.nChannels))
        self.rectifiedData = np.empty((self.nSamples, self.nChannels))
        self.counter = 0 
        

    def addSample(self, newSample):
        # numpy.roll 
        # FIFO buffer 
        # pop data from the array and push new sample 
        self.rawDataBuffer = np.roll(self.rawDataBuffer, -1, axis = 0)
        self.rawDataBuffer[-1,:] = newSample
        self.counter += 1

        if self.counter >= np.shape(self.rawData)[0]:
            # if you run out of space in the initialed, add more empty sapce
            self.rawData = np.append(self.rawData, np.empty((self.largeInitializedSpace, self.nChannels)))

 

    def bandpassFilterData(self, bpLowCutoff, bpHighCutoff, order):
        b, a = scipy.signal.butter(order, [bpLowCutoff, bpHighCutoff], 'bandpass',fs=self.samplingRate)
        self.bpFilteredData = scipy.signal.filtfilt(b, a, self.rawDataBuffer, axis = 0)

    def rectifyData(self):
        self.rectifiedData = abs(self.bpFilteredData)

    def lowpassFilterData(self, lpHIghCutoff, order):
        b, a = scipy.signal.butter(order, lpHIghCutoff, 'lowpass',fs=self.samplingRate) 
        self.lpFilteredData = scipy.signal.filtfilt(b, a, self.rectifiedData, axis = 0)

    def takeMean(self):
        self.meanData = np.mean(self.lpFilteredData) # currently the mean of the whole nSamples AND ALL CHANNELS 
        # This could be reduced to only be the most recent samples (such as the most recent filterAfterN samples)

    def processBuffer(self, bpLowCutoff, bpHighCutoff, lpHIghCutoff, order):
        self.bandpassFilterData(bpLowCutoff, bpHighCutoff, order)
        self.rectifyData()
        self.lowpassFilterData(lpHIghCutoff, order)
        self.takeMean()


    def save(self, filename):
        np.savetxt(filename, self.rawData)

