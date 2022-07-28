from statistics import mean
from tkinter import NS
import numpy as np 
import scipy.signal
import math


class processData:

    def __init__(self, nChannels, nDataChannels, samplingRate, nSamples, filterAfterN, cueChannel, largeInitializedSpace = 1000000): 
        self.nSamples = nSamples
        print('Length of buffer set to:', nSamples)
        self.nChannels = nChannels
        print('Channels to record:', nChannels)
        self.nDataChannels = nDataChannels
        print('Channels of EMG data to record:', self.nDataChannels)
        self.filterAfterN = filterAfterN
        self.samplingRate = samplingRate
        self.cueChannel = cueChannel

        self.largeInitializedSpace = largeInitializedSpace #### this is arbitary 
        self.rawData = np.empty((self.largeInitializedSpace, self.nChannels))
        self.rawDataBuffer = np.empty((self.nSamples, self.nDataChannels))
        # self.bpFilteredData = np.empty((self.nSamples, self.nDataChannels))
        # self.lpFilteredData = np.empty((self.nSamples, self.nDataChannels))
        self.rectifiedData = np.empty((self.nSamples, self.nDataChannels))
        self.MvcMean = np.empty((2500))
        self.MvcCue = np.empty((2500))
        self.counter = 0 
        self.MvcCounter = 0
        self.thresholdCrossed = False
        self.thresholdCrossedHistory = np.full((math.ceil(self.nSamples/self.filterAfterN)), False)
        print(self.thresholdCrossedHistory)

    def addSample(self, newSample):
        # numpy.roll 
        # FIFO buffer 
        # pop data from the array and push new sample 
        self.rawDataBuffer = np.roll(self.rawDataBuffer, -1, axis = 0)
        self.rawDataBuffer[-1,:] = newSample[:self.nDataChannels]
        self.rawData[self.counter, :] = newSample
        self.counter += 1

        if self.counter >= np.shape(self.rawData)[0]:
            # if you run out of space in the initialed, add more empty sapce
            self.rawData = np.append(self.rawData, np.empty((self.largeInitializedSpace, self.nChannels)))

 

    def bandpassFilterData(self, bpLowCutoff, bpHighCutoff, order):
        sos = scipy.signal.butter(order, [bpLowCutoff, bpHighCutoff], 'bandpass', output='sos',fs=self.samplingRate)
        self.bpFilteredData = scipy.signal.sosfiltfilt(sos, self.rawDataBuffer, axis = 0, padtype=None, padlen=0)


    def rectifyData(self):
        self.rectifiedData = abs(self.bpFilteredData)

    def lowpassFilterData(self, lpHIghCutoff, order):
        sos = scipy.signal.butter(order, lpHIghCutoff, 'lowpass', output='sos',fs=self.samplingRate) 
        self.lpFilteredData = scipy.signal.sosfiltfilt(sos, self.rectifiedData, axis = 0, padtype=None, padlen=0)

    def takeMean(self, filter_after_n):
        self.meanData = np.mean(self.lpFilteredData[-filter_after_n:, :])
        # print(self.meanData)
        # This could be reduced to only be the most recent samples (such as the most recent filterAfterN samples)
    
    def thresholdCross(self, filter_after_n, mvc_threshold):
        # print("raw:", self.rawDataBuffer)
        # print("data:", self.lpFilteredData)
        threshold_crossings = np.diff(np.squeeze(self.lpFilteredData[50:-25]) > mvc_threshold) # [-filter_after_n:, :]
        # print("threshold croessings", threshold_crossings)
        positive_difference = np.diff(np.squeeze(self.lpFilteredData[50:-25])) > 0 #[-filter_after_n:, :]
        # print("positive diff", positive_difference)
        self.thresholdCrossed =  np.any(np.logical_and(threshold_crossings, positive_difference))

        if self.thresholdCrossed == True:
            print("crossed!")
        else:
            print(":(")

        self.thresholdCrossedHistory = np.roll(self.thresholdCrossedHistory, -1, axis = 0)
        
        if self.thresholdCrossedHistory.any():
            self.thresholdCrossed = False
            print('negated')

        self.thresholdCrossedHistory[-1] = self.thresholdCrossed
        print(self.thresholdCrossedHistory)
        


    def cueStatus(self, filter_after_n):
        # print("counter:", self.counter, "minus:", self.counter-filter_after_n)
        # print("channel:", self.cueChannel)
        # print(self.rawData[self.counter-filter_after_n:self.counter, self.cueChannel])
        self.cue = (self.rawData[self.counter-filter_after_n:self.counter, self.cueChannel] == 0).any()

    def processBuffer(self, bpLowCutoff, bpHighCutoff, lpHIghCutoff, order, filter_after_n, mvc_threshold):
        self.bandpassFilterData(bpLowCutoff, bpHighCutoff, order)
        self.rectifyData()
        self.lowpassFilterData(lpHIghCutoff, order)
        self.cueStatus(filter_after_n)
        self.takeMean(filter_after_n)
        self.thresholdCross(filter_after_n, mvc_threshold) 


    def save(self, filename):
        np.savetxt(filename, self.rawData)
        print("The data was saved to:", filename)


    def processMVC(self, bpLowCutoff, bpHighCutoff, lpHIghCutoff, order, filter_after_n):

        self.bandpassFilterData(bpLowCutoff, bpHighCutoff, order)
        self.rectifyData()
        self.lowpassFilterData(lpHIghCutoff, order)
        self.cueStatus(filter_after_n)
        self.takeMean(filter_after_n)

        self.MvcMean[self.MvcCounter] = self.meanData
        print("%.2f" % self.meanData, self.cue)
        self.MvcCue[self.MvcCounter] = self.cue
        self.MvcCounter += 1
    
    def maxMVC(self):
        print(self.MvcMean)
        print(self.MvcCue)

        cue_diff = np.diff(self.MvcCue)
        # print(cue_diff)
        self.MvcCue[np.argmax(cue_diff == 1):np.argmax(cue_diff == -1)] = 1
        print(np.argmax(cue_diff == 1))
        print(np.argmax(cue_diff == -1))
        max_MVC = np.max(self.MvcMean[self.MvcCue == 0])
        print('The max of the MVC was:', max_MVC)
        return max_MVC