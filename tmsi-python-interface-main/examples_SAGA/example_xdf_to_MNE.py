'''
Copyright 2021 Twente Medical Systems international B.V., Oldenzaal The Netherlands

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#######  #     #   #####   #  ######      #     #
   #     ##   ##  #        #  #     #     #     #
   #     # # # #  #        #  #     #     #     #
   #     #  #  #   #####   #  ######       #   #
   #     #     #        #  #  #     #      #   #
   #     #     #        #  #  #     #       # #
   #     #     #  #####    #  ######   #     #     #

Example : This example shows how to read data from a Xdf-file to an MNE-object. 

'''

import sys
sys.path.append("../")
import mne

from TMSiSDK.file_readers import Xdf_Reader

reader=Xdf_Reader(add_ch_locs=False)
# When no filename is given, a pop-up window allows you to select the file you want to read. 
# You can also use reader=Xdf_Reader(full_path) to load a file. Note that the full file path is required here.
# add_ch_locs can be used to include TMSi EEG channel locations (in case xdf-file does not contain channel locations)

# An XDF-file can consist of multiple streams. The output data is of the tuple type, to allow for multi stream files.
mne_object, timestamps = reader.data, reader.time_stamps

# Extract data from the first stream
samples = mne_object[0]._data


#%%
mne_object[0].plot_sensors(ch_type='eeg', show_names=True) 
mne_object[0].plot(start=0, duration=5, n_channels=5, title='Xdf Plot') 