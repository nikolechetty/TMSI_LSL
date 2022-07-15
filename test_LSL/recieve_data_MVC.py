"""Rudimentary program to show how to read and filter a single-channel 
time series from LSL an provide haptic feedback."""

from pylsl import StreamInlet, resolve_stream, StreamInfo
from buffer_trigger_filter import *
import time
from ctypes import *
import os
from datetime import datetime
import threading

NUM_SAMPLES_BUFFER = 400
FILTER_AFTER_N = 200
BP_LOW_CUTOFF = 20
BP_HIGH_CUTOFF = 500
ORDER = 5
LP_HIGH_CUTOFF = 10
DATA_CHANNELS = 1 # the channels up to this number will be considered EMG and processed 
CUE_CHANNEL = 4


def main():

    try:
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streams = resolve_stream('type', 'EEG')

        for info in streams:
            print('name: ', info.name())
            print('channel count:', info.channel_count())
            print('sampling rate:', info.nominal_srate())
            print('type: ', info.type())

        # create a new inlet to read from the stream
        inlet = StreamInlet(streams[0]) # This is only looking for ONE stream, the first one found


        time.sleep(2) # Added so I can see the info data before data starts streaming

        process_data = processData(nChannels = streams[0].channel_count(), samplingRate = streams[0].nominal_srate(), nSamples = NUM_SAMPLES_BUFFER, 
            nDataChannels = DATA_CHANNELS, cueChannel = CUE_CHANNEL, filterAfterN = FILTER_AFTER_N)


        while True:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample, timestamp = inlet.pull_sample()
            # print(timestamp, sample)
            process_data.addSample(sample)

            
            if process_data.counter % process_data.filterAfterN == 0:
                process_data.processMVC(BP_LOW_CUTOFF, BP_HIGH_CUTOFF, LP_HIGH_CUTOFF, ORDER, FILTER_AFTER_N)
                # print(process_data.MvcMean) #"%.2f" % 




    finally: # except KeyboardInterrupt
        process_data.maxMVC()
        # print("The max MVC was:", max_MVC)

        # Save the raw data to a file
        timestr = time.strftime("%Y%m%d-%H%M%S")
        save_name = "raw_data_MVC_" + timestr
        process_data.save(save_name)

        print()



if __name__ == '__main__':
    main()