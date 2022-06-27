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

Example : This example shows the functionality to stream to LSL.

'''

import sys
sys.path.append("../")

from PySide2 import QtWidgets

from TMSiSDK import tmsi_device
from TMSiSDK import plotters
from TMSiSDK.device import DeviceInterfaceType, DeviceState
from TMSiSDK.file_writer import FileWriter, FileFormat
from TMSiSDK.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable



try:
    # Initialise the TMSi-SDK first before starting using it
    tmsi_device.initialize()
    
    # Create the device object to interface with the SAGA-system.
    dev = tmsi_device.create(tmsi_device.DeviceType.saga, DeviceInterfaceType.docked, DeviceInterfaceType.usb)
    
    # Find and open a connection to the SAGA-system and print its serial number
    dev.open()  
    
    # Check if there is already a plotter application in existence
    plotter_app = QtWidgets.QApplication.instance()
    
    # Initialise the plotter application if there is no other plotter application
    if not plotter_app:
        plotter_app = QtWidgets.QApplication(sys.argv)
    
    # Initialise the lsl-stream
    stream = FileWriter(FileFormat.lsl, "SAGA")
    
    # Define the handle to the device
    stream.open(dev)

    # Define the GUI object and show it 
    # The channel selection argument states which channels need to be displayed initially by the GUI
    plot_window = plotters.RealTimePlot(figurename = 'A RealTimePlot', 
                                        device = dev, 
                                        channel_selection = [0,1,2])
    plot_window.show()
    
    # Enter the event loop
    plotter_app.exec_()
    
    # Quit and delete the Plotter application
    QtWidgets.QApplication.quit()
    del plotter_app
    
    # Close the file writer after GUI termination
    stream.close()
    
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