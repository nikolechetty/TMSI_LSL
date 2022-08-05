from statistics import mean
from tkinter import NS
import numpy as np 
import scipy.signal


class postProcessData:

    def __init__(self, samplingRate, rawData): 

        self.nDataChannels = 1 #np.shape(rawData)[1]
        self.samplingRate = samplingRate
        self.lengthData = np.shape(rawData)[0]
        self.rawData = rawData

        self.bpFilteredData = np.empty((self.lengthData, self.nDataChannels))
        self.lpFilteredData = np.empty((self.lengthData, self.nDataChannels))
        self.rectifiedData = np.empty((self.lengthData, self.nDataChannels))
        self.meanData = np.empty((self.lengthData, self.nDataChannels))


    def bandpassFilterData(self, bpLowCutoff, bpHighCutoff, order):
        sos = scipy.signal.butter(order, [bpLowCutoff, bpHighCutoff], 'bandpass', output='sos',fs=self.samplingRate)
        self.bpFilteredData = scipy.signal.sosfiltfilt(sos, self.rawData, axis = 0)

    def rectifyData(self):
        self.rectifiedData = abs(self.bpFilteredData)

    def lowpassFilterData(self, lpHIghCutoff, order):
        sos = scipy.signal.butter(order, lpHIghCutoff, 'lowpass', output='sos',fs=self.samplingRate) 
        self.lpFilteredData = scipy.signal.sosfiltfilt(sos, self.rectifiedData, axis = 0)

    def movingMean(self, filter_after_n):
        self.meanData = np.convolve(self.lpFilteredData, np.ones(filter_after_n), 'valid') / filter_after_n
        

    def processAll(self, bpLowCutoff, bpHighCutoff, lpHIghCutoff, order, filter_after_n):
        self.bandpassFilterData(bpLowCutoff, bpHighCutoff, order)
        self.rectifyData()
        self.lowpassFilterData(lpHIghCutoff, order)
        self.movingMean(filter_after_n)


    def save(self, filename):
        np.savetxt(filename, self.rawData)
        print("The data was saved to:", filename)

