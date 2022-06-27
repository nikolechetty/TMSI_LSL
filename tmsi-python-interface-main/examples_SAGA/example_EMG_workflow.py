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

Example : This example shows the functionality of the impedance plotter and an
            HD-EMG heatmap. The user has to configure the tail orientation of 
            the grid, so that the grid is adapted to 'look into the grid'. The
            heatmap displays the RMS value per channel, combined with linear 
            interpolation to fill the space between channels.

'''

import sys
sys.path.append("../")
import time

from PySide2 import QtWidgets

from TMSiSDK import tmsi_device
from TMSiSDK import plotters
from TMSiSDK.device import DeviceInterfaceType, DeviceState
from TMSiSDK.file_writer import FileWriter, FileFormat
from TMSiSDK.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK import get_config


try:
    # Initialise the TMSi-SDK first before starting using it
    tmsi_device.initialize()
    
    # Create the device object to interface with the SAGA-system.
    dev = tmsi_device.create(tmsi_device.DeviceType.saga, DeviceInterfaceType.docked, DeviceInterfaceType.usb)
    
    # Find and open a connection to the SAGA-system and print its serial number
    dev.open()
    
    # Load the EEG channel set and configuration
    print("load HD-EMG config")
    if dev.config.num_channels<64:
        cfg = get_config("saga_config_32UNI")
    else:
        cfg = get_config("saga_config_64UNI")
    dev.load_config(cfg)
    
    
    # Check if there is already a plotter application in existence
    plotter_app = QtWidgets.QApplication.instance()
    
    # Initialise the plotter application if there is no other plotter application
    if not plotter_app:
        plotter_app = QtWidgets.QApplication(sys.argv)
        
    # Define the GUI object and show it
    window = plotters.ImpedancePlot(figurename = 'An Impedance Plot', device = dev, layout = 'grid', file_storage = True)
    window.show()
    
    # Enter the event loop
    plotter_app.exec_()
    
    # Pause for a while to properly close the GUI after completion
    print('\n Wait for a bit while we close the plot... \n')
    time.sleep(1)
    
    # Ask for desired file format
    file_format=input("Which file format do you want to use? (Options: poly5 or xdf)\n")
    
    # Initialise the desired file-writer class and state its file path
    if file_format.lower()=='poly5':
        file_writer = FileWriter(FileFormat.poly5, "../measurements/example_EMG_workflow.poly5")
    elif file_format.lower()=='xdf':
        file_writer = FileWriter(FileFormat.xdf, "../measurements/example_EMG_workflow.xdf", add_ch_locs=True)
    else:
        print('File format not supported. File is saved to Poly5-format.')
        file_writer = FileWriter(FileFormat.poly5, "../measurements/example_EMG_workflow.poly5")
    
    # Define the handle to the device
    file_writer.open(dev)

    # Define the GUI object and show it 
    # The tail orientation is needed so that the user looks 'into' the grid. 
    # The signal_lim parameter (in microVolts) is needed to configure the colorbar range
    plot_window = plotters.HDEMGPlot(figurename = 'An HD-EMG Heatmap', 
                                        device = dev,
                                        tail_orientation = 'down',
                                        signal_lim = 350)
    plot_window.show()
    
    # Enter the event loop
    plotter_app.exec_()
    
    # Quit and delete the Plotter application
    QtWidgets.QApplication.quit()
    del plotter_app
    
    # Close the file writer after GUI termination
    file_writer.close()
    
    # Close the connection to the SAGA device
    dev.close()
    
except TMSiError as e:
    print("!!! TMSiError !!! : ", e.code)
    if (e.code == TMSiErrorCode.device_error) :
        print("  => device error : ", hex(dev.status.error))
        DeviceErrorLookupTable(hex(dev.status.error))
        
finally:
    # Close the connection to the device when the device is opened
    if dev.status.state == DeviceState.connected:
        dev.close()