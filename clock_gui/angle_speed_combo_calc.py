# Analog clock with callback function
                            
from math import *
from time import *
import ctypes
from datetime import datetime 
import itertools
import random 
import numpy as np
import matplotlib.pyplot as plt


# ANGLES = [17, 30, 43.5] # small, medium, and large targets 
# SPEED = [18, 27, 35] # slow, medium, and fast cursor speeds



# #Determine combinations of angle and speed to display
# combinations = list(itertools.product(ANGLES, SPEED))
# # print(combinations)
# random.shuffle(combinations)
# print("Angle/Speed combinations:", combinations)

# Wt_array = np.empty(1)
# Dt_array = np.empty(1)
# ID_array = np.empty(1)

# for combos in combinations:

#     angle_width = combos[0]
#     hand_speed = combos[1]
#     print('Angle width:', angle_width, 'Hand speed:', hand_speed)

#     Wt = angle_width/hand_speed/360*60*1000 # in millisec
#     Wt_array = np.append(Wt_array, Wt)
    
#     Dt = (360)/hand_speed/360*60*1000 # in millisec #(360 - angle_width)/hand_speed/360*60*1000
#     Dt_array = np.append(Dt_array, Dt)

#     ID = log2(Dt/Wt)
#     ID_array = np.append(ID_array, ID)
#     print('Wt:', "%.2f" % Wt, 'ms, Dt:',"%.2f" % Dt, 'ms, ID:', ID,'bits')
            
# plt.scatter(Wt_array[1:], Dt_array[1:])
# plt.title('Levels of Wt and Dt')
# plt.xlabel('Target Width (ms)')
# plt.ylabel('Temporal Distance (ms)')
# plt.show()

# plt.scatter(ID_array[1:], np.zeros(np.size(ID_array[1:])), alpha=0.5)
# plt.show()

##############################

W_t = [60, 150, 220] # small, medium, and large targets 
D_t = [1000, 1600, 2200] # slow, medium, and fast cursor speeds



#Determine combinations of angle and speed to display
combinations = list(itertools.product(W_t, D_t))
# print(combinations)
random.shuffle(combinations)
print("Wt/Dt combinations:", combinations)

Angles_array = np.empty(1)
Speeds_array = np.empty(1)
ID_array = np.empty(1)

for combos in combinations:

    Wt = combos[0]
    Dt = combos[1]
    print('Wt:', Wt, 'Dt:', Dt)

    hand_speed = 1/Dt*60*1000 # in rev/min
    angle_width = Wt*hand_speed/60*360/1000



    Angles_array = np.append(Angles_array, angle_width)
    Speeds_array = np.append(Speeds_array, hand_speed)

    ID = log2(Dt/Wt)
    ID_array = np.append(ID_array, ID)
    print('Angle:', "%.2f" % angle_width, 'ms, Speed:',"%.2f" % hand_speed, 'ms, ID:', ID,'bits')
            
plt.scatter(Angles_array[1:], Speeds_array[1:])
plt.title('Levels of angles and speeds')
plt.xlabel('Angle (deg')
plt.ylabel('Speed (rev/min)')
plt.show()

plt.scatter(ID_array[1:], np.zeros(np.size(ID_array[1:])), alpha=0.5)
plt.show()

print(ID_array)
print(np.round(np.sort(ID_array), 2))