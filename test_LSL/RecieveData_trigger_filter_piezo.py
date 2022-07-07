"""Rudimentary program to show how to read and filter a single-channel 
time series from LSL an provide haptic feedback."""

from pylsl import StreamInlet, resolve_stream, StreamInfo
from buffer_trigger_filter import *
import time
from ctypes import *
import os

NUM_SAMPLES_BUFFER = 1000
FILTER_AFTER_N = 500
BP_LOW_CUTOFF = 20
BP_HIGH_CUTOFF = 500
ORDER = 5
LP_HIGH_CUTOFF = 10

TACTOR_ID = 1 
TACTOR_PULSE_WIDTH = 50 # ms ##### Should not be larger than (filter_after_n/sampling_rate*1000)
TACTOR_DELAY = 0 # ms
PULSE_THRESHOLD = 10 #muV

def main():

    try: 
        current_folder = os.path.dirname(os.path.abspath(__file__))
        rel_path = 'Windows_x64\TactorInterface.dll'
        dllPath = os.path.join(current_folder, rel_path)


        devicePort = "COM3"

        tdk = windll.LoadLibrary(dllPath)

        tdk.InitializeTI()

        tdk.Connect.argtypes = [c_char_p, c_int, c_void_p]
        device = tdk.Connect(c_char_p(devicePort.encode("ascii")), 0x01, None)

        if device == -1:
            print("Failed to connect, error:", tdk.GetLastEAIError())
        else:
            print("Connected!")


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
            filterAfterN = FILTER_AFTER_N)

        while True:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample, timestamp = inlet.pull_sample()
            # print(timestamp, sample)
            process_data.addSample(sample)

            
            if process_data.counter % process_data.filterAfterN == 0:
                process_data.processBuffer(BP_LOW_CUTOFF, BP_HIGH_CUTOFF, LP_HIGH_CUTOFF, ORDER)
                print("%.2f" % process_data.meanData)

                # Add pulse to the peizotac system 
                if process_data.meanData > PULSE_THRESHOLD:
                    tdk.Pulse(device, TACTOR_ID, TACTOR_PULSE_WIDTH, TACTOR_DELAY)


    finally: # except KeyboardInterrupt
        # Save the raw data to a file
        timestr = time.strftime("%Y%m%d-%H%M%S")
        save_name = "raw_data_" + timestr
        process_data.save(save_name)

        # Shutdown the connection to the piezotac
        tdk.UpdateTI()
        time.sleep(0.5)
        tdk.Close(device)
        print("Disconnected.")
        tdk.ShutdownTI()



if __name__ == '__main__':
    main()