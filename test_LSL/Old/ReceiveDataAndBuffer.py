"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream, StreamInfo
from buffer_data import *
import time




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

    process_data = processData(nChannels = streams[0].channel_count(), samplingRate = streams[0].nominal_srate(), nSamples = 1000, 
        filterAfterN = 100, bpLowCutoff = 5, bpHighCutoff = 40, order = 5)

    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        print(timestamp, sample)
        process_data.addSample(sample)





if __name__ == '__main__':
    main()