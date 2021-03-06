"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream, StreamInfo
from buffer_trigger_filter import *
import time

NUM_SAMPLES_BUFFER = 1000
FILTER_AFTER_N = 100
BP_LOW_CUTOFF = 5 
BP_HIGH_CUTOFF = 40 
ORDER = 5
LP_HIGH_CUTOFF = 5


def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    
    for info in streams:
        print('name: ', info.name())
        print('channel count:', info.channel_count())
        print('sampling rate:', info.nominal_srate())
        print('type: ', info.type())

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0]) # This is only looking for ONE stream


    time.sleep(2) # Added so I can see the info data before data starts streaming

    process_data = processData(nChannels = streams[0].channel_count(), samplingRate = streams[0].nominal_srate(), nSamples = NUM_SAMPLES_BUFFER, 
        filterAfterN = FILTER_AFTER_N)

    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        # print(timestamp, sample)
        process_data.addSample(sample)

        
        if process_data.counter % process_data.filterAfterN == 0:
            process_data.processBuffer(BP_LOW_CUTOFF, BP_HIGH_CUTOFF, LP_HIGH_CUTOFF, ORDER)
            print(process_data.meanData)




if __name__ == '__main__':
    main()