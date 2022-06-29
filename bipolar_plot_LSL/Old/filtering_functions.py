
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.signal
import warnings


def bandpass_filter(data, low_freq, high_freq, order, sampling_rate):
    """
    Bandpass filters rows of dataframe.

    Parameters
    ----------
    data : df
        Dataframe to filter. Channels x samples
    low_freq : int
        Low critical frequency. Must be lower than sampling_rate.
   high_freq : int
        High critical frequency. Must be lower than sampling_rate.
    order : int
        Filter order
    sampling_rate :
        Sampling rate of the data to be filtered (Hz).

        
    Returns
    -------
    df
        Dataframe with bandpass filtered rows.

    """
    b, a = scipy.signal.butter(order, [low_freq, high_freq], 'bandpass',fs=sampling_rate) #analog=True
    bandpass_filtered_data = scipy.signal.filtfilt(b, a, data)
    
    # #For filter stats:
    # print('b:', b)
    # print('a:', a)
    
    return bandpass_filtered_data