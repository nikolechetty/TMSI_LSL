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

Example : This example shows the different configuration options, more detailed 
explanations can be found in the examples of individual properties


'''


import sys
sys.path.append("../")
from PySide2 import QtWidgets

from TMSiSDK import tmsi_device
from TMSiSDK import plotters
from TMSiSDK.device import DeviceInterfaceType, DeviceState, ChannelType, ReferenceMethod, ReferenceSwitch
from TMSiSDK.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable



try:
    # Initialise the TMSi-SDK first before starting using it
    tmsi_device.initialize()
    
    # Create the device object to interface with the SAGA-system.
    dev = tmsi_device.create(tmsi_device.DeviceType.saga, DeviceInterfaceType.docked, DeviceInterfaceType.usb)
    
    # Find and open a connection to the SAGA-system and print its serial number
    dev.open()
    
    # Print current device configuation
    print('Current device configuration:')
    print('Base-sample-rate: \t\t\t{0} Hz'.format(dev.config.base_sample_rate))
    print('Sample-rate: \t\t\t\t{0} Hz'.format(dev.config.sample_rate))
    print('Reference Method: \t\t\t', dev.config.reference_method)
    print('Sync out configuration: \t', dev.config.get_sync_out_config())
    print('Triggers:\t\t\t\t\t', dev.config.triggers )
    
    # Update the different configuration options:
    
    # Set base sample rate: either 4000 Hz (default)or 4096 Hz.
    dev.config.base_sample_rate = 4000
    
    # Set sample rate to 2000 Hz (base_sample_rate/2)
    dev.config.set_sample_rate(ChannelType.all_types, 2)
    
    # Specify the reference method and reference switch method that are used during sampling 
    dev.config.reference_method = ReferenceMethod.common,ReferenceSwitch.fixed
    
    # Set the trigger settings
    dev.config.triggers=True
    
    # Set the sync out configuration
    dev.config.set_sync_out_config(marker=False, freq=1, duty_cycle=50)

    # Print new device configuation
    print('\n\nNew device configuration:')
    print('Base-sample-rate: \t\t\t{0} Hz'.format(dev.config.base_sample_rate))
    print('Sample-rate: \t\t\t\t{0} Hz'.format(dev.config.sample_rate))
    print('Reference Method: \t\t\t', dev.config.reference_method)
    print('Sync out configuration: \t', dev.config.get_sync_out_config())
    print('Triggers:\t\t\t\t\t', dev.config.triggers )
    
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