# Analog clock with callback function
from tkinter import *                                 
from math import *
from time import *
import ctypes
from datetime import datetime
import serial 
import itertools
import random 
from pylsl import StreamInlet, resolve_stream
import numpy as np 


# Improve resolution of Tkinter canvas
ctypes.windll.shcore.SetProcessDpiAwareness(1)



WT = [150] # small, medium, and large targets #60, 150, 
DT = [1000, 1600, 2200] # slow, medium, and fast cursor speeds

START_ANGLE = 180         # 0 deg is north, degrees go clockwise for positive

NUM_ROTATIONS = 25
CANVAS_SIZE = 2000

BLUE_FILL = "#79d2f2"
CORRECT_FILL = "green"



#Determine combinations of angle and speed to display
combinations = list(itertools.product(WT, DT))
# print(combinations)
random.shuffle(combinations)
print("Wt/Dt combinations:", combinations)



# Open LSL Stream
print("looking for a marker stream...")
streams = resolve_stream('type', 'Markers')
# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])
chunk, timestamps = inlet.pull_chunk()
if timestamps:
    print("got %s at time %s" % (chunk, timestamps))

#Open serial port for comminication of digitial out
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)



class ClockGUI():
    def __init__(self, combinations): 
        self.combination_counter = 0

        Wt = combinations[self.combination_counter][0]
        Dt = combinations[self.combination_counter][1]
        
        self.hand_speed = 1/Dt*60*1000 # in rev/min
        self.angle_width = Wt*self.hand_speed/60*360/1000
        
        print('Wt:', "%.2f" % Wt, 'ms, Dt:',"%.2f" % Dt, 'ms, ID:', log2(Dt/Wt),'bits')
        print('Angle width:', self.angle_width, 'Hand speed:', self.hand_speed)


        self.rotation_counter = 0
        self.target_trigger = False
        self.num_combinations = len(combinations)
        self.phi_deg_prev, self.phi_rad_prev = self.getAngle()
        self.phi_deg, self.phi_rad = self.getAngle()
        self.start_at_zero = False
        self.execute = False
        self.fill = BLUE_FILL

    def getAngle(self):
        dt = datetime.now()
        t_s_with_micros =  (dt.second + dt.microsecond/1e6)*self.hand_speed
        phi_micros_rad = (pi/30 * t_s_with_micros) 
        phi_micros_degrees = 360/60 * t_s_with_micros % 360
        return phi_micros_degrees, phi_micros_rad

    def updateClock(self, w, nx, ny, guiClass):  # clock draw function
        # helper variables 
        x0 = nx/2; lx = 9*nx/20     # center and half-width of clock face
        y0 = ny/2; ly = 9*ny/20
        r2 = 0.8 * min(lx,ly)   # length of hand

        # create outline of circle
        w.create_oval(x0-lx, y0-ly, x0+lx, y0+ly, width=6)  # clock face

        # create the target area
        starting_formula = -(START_ANGLE-90)
        w.create_arc(x0-lx, y0-ly, x0+lx, y0+ly, start=starting_formula, extent=-self.angle_width, style=PIESLICE, fill=self.fill)

        # Use the time to create smooth movement of the clock hand

        self.phi_deg, self.phi_rad = self.getAngle()
        # print(self.phi_deg)
        if self.start_at_zero == False: 

            if self.phi_deg >= 5:
                self.phi_deg, self.phi_rad = 0, 0 
            else: 
                self.start_at_zero = True


        x = x0 + r2 * sin(self.phi_rad)   # position of end of the arrowhead
        y = y0 - r2 * cos(self.phi_rad)
        w.create_line(x0, y0 , x, y, arrow=LAST, width=8)       # draw hand


        # print('Angle of hand:', self.phi_deg)
        # print('Time:',"%.2f" % t_s_with_micros, 'Angle deg:',"%.2f" %  phi_micros_degrees, 'Angle rad:', "%.2f" % phi_micros_rad)
        #    print("x:", x, ", y:", y)

        # know whether you are in the target or not
        if self.phi_deg >= START_ANGLE and self.phi_deg <= (START_ANGLE+self.angle_width):
            # print("You're in the target!")
            # write the signal to the ardunio 
            arduino.write(bytes([1]))
            # print(arduino.readline()) # remove print statement when running real exp
            self.target_trigger = True

        else:
            # message = bytes(0, 'utf-8')
            arduino.write(bytes([0]))
            # print(arduino.readline())

            # when first exiting the target -> add one rotation\
            if self.target_trigger == True:
                self.rotation_counter += 1 
                print('ROTATIONS:',self.rotation_counter)
            self.target_trigger = False

        if self.phi_deg <= 10:
            #reset fill to blue at the at north position
            self.fill = BLUE_FILL

        if self.rotation_counter >= NUM_ROTATIONS and self.phi_deg <= 25:
            # more than X rotations and passes zero, swtich to the next combination
            
            self.combination_counter += 1
            if  self.combination_counter <= self.num_combinations - 1:
                Wt = combinations[self.combination_counter][0]
                Dt = combinations[self.combination_counter][1]
                
                self.hand_speed = 1/Dt*60*1000 # in rev/min
                self.angle_width = Wt*self.hand_speed/60*360/1000
                
                print('Wt:', "%.2f" % Wt, 'ms, Dt:',"%.2f" % Dt, 'ms, ID:', log2(Dt/Wt),'bits')
                print('Angle width:', self.angle_width, 'Hand speed:', self.hand_speed)

                self.rotation_counter = 0  
                self.start_at_zero = False

                # pause screen for a little bit - indicate change 
                w.delete(ALL)
                # root.after(10, self.freezeGUI(w, nx, ny, guiClass)) # need to pause
 
            else:
                root.after(2000, root.destroy)

        # pull sample from LSL 
        chunk, timestamps = inlet.pull_chunk()
        if timestamps:
            # print("got %s at time %s" % (chunk, timestamps))
            # print(type(chunk))
            if CORRECT_FILL in chunk[0]:
                self.fill = CORRECT_FILL

    def freezeGUI(self, w, nx, ny, guiClass):
        w.delete(ALL)
        w.after(150, Clock, w, nx, ny, guiClass) # need to pause


def Clock(w, nx, ny, guiClass):                                # clock callback function
    w.delete(ALL)                                              # delete canvas
    guiClass.updateClock(w, nx, ny, guiClass)                                        # draw clock
    w.after(18, Clock, w, nx, ny, guiClass)                  # call callback after 5 ms




# Main

root = Tk()                                           # create Tk root widget
root.title("Python clock")

nx = CANVAS_SIZE; ny = CANVAS_SIZE                                            # canvas size
w = Canvas(root, width=nx, height=ny, bg = "white")         # create canvas w
w.pack()                                                # make canvas visible

gui = ClockGUI(combinations)

Clock(w, nx, ny, gui)                                        # call clock function
# root.after(ACTIVE_TIME, root.destroy)         # close window after given time
root.mainloop()                                    # enter Tkinter event loop


timestr = strftime("%Y%m%d-%H%M%S")
save_name = "combo_info_" + timestr +'.npz'
np.savez(save_name, combos = combinations, reps = NUM_ROTATIONS)
print("Data has been saved to:", save_name)
