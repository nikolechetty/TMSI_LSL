# Analog clock with callback function
from tkinter import *                                 # import Tkinter module
from math import *
from time import *
import ctypes
from datetime import datetime
import serial 
import itertools
import random 

ctypes.windll.shcore.SetProcessDpiAwareness(1)

arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

ANGLES = [10, 20] # small, medium, and large targets 
SPEED = [5, 10] # slow, medium, and fast cursor speeds

START_ANGLE = 90         # 0 deg is north, degrees go clockwise for positive
# EXTENT_ANGLE = 60
# ACTIVE_TIME = 20000 # 20 seconds

NUM_ROTATIONS = 2



combinations = list(itertools.product(ANGLES, SPEED))
# print(combinations)
random.shuffle(combinations)
print("Angle/Speed combinations:", combinations)

# combination_counter = 0
# angle_width = combinations[combination_counter][0]
# print(angle_width)
# hand_speed = combinations[combination_counter][1]
# print(hand_speed)

# target_trigger = False
# speed_factor = 3


class ClockGUI():
    def __init__(self, combinations): 
        self.combination_counter = 0
        self.angle_width = combinations[self.combination_counter][0]
        print('Angle width', self.angle_width)
        self.hand_speed = combinations[self.combination_counter][1]
        print('Hand speed', self.hand_speed)

        self.rotation_counter = 0
        self.target_trigger = False
        self.num_combinations = len(combinations)

    def updateClock(self, w, nx, ny):  # clock draw function
        # helper variables 
        x0 = nx/2; lx = 9*nx/20     # center and half-width of clock face
        y0 = ny/2; ly = 9*ny/20
        r2 = 0.8 * min(lx,ly)   # length of hand

        # create outline of circle
        w.create_oval(x0-lx, y0-ly, x0+lx, y0+ly, width=2)  # clock face

        # create the target area
        starting_formula = -(START_ANGLE-90)
        w.create_arc(x0-lx, y0-ly, x0+lx, y0+ly, start=starting_formula, extent=-self.angle_width, style=PIESLICE, fill="blue")

        # Use the time to create smooth movement of the clock hand
        dt = datetime.now()
        t_s_with_micros =  (dt.second + dt.microsecond/1e6)*self.hand_speed
        phi_micros_rad = (pi/30 * t_s_with_micros) 
        phi_micros_degrees = 360/60 * t_s_with_micros % 360


        x = x0 + r2 * sin(phi_micros_rad)   # position of end of the arrowhead
        y = y0 - r2 * cos(phi_micros_rad)
        w.create_line(x0, y0 , x, y, arrow=LAST, width=4)       # draw hand
        # print('Angle of hand:', phi_degrees)
        # print('Time:',"%.2f" % t_s_with_micros, 'Angle deg:',"%.2f" %  phi_micros_degrees, 'Angle rad:', "%.2f" % phi_micros_rad)
        #    print("x:", x, ", y:", y)

        # know whether you are in the target or not
        if phi_micros_degrees >= START_ANGLE and phi_micros_degrees <= (START_ANGLE+self.angle_width):
            print("You're in the target!")
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

        if self.rotation_counter >= NUM_ROTATIONS:
            # more than X rotations
            
            # pause screen for a little bit - indicate change 
            # root.after(5000) # need to pause

            # swtich to the next combination
            
            self.combination_counter += 1
            if  self.combination_counter <= self.num_combinations - 1:
                self.angle_width = combinations[self.combination_counter][0]
                print('Angle width', self.angle_width)
                self.hand_speed = combinations[self.combination_counter][1]
                print('Hand speed', self.hand_speed)

                self.rotation_counter = 0   
            else:
                root.after(1000, root.destroy)


def Clock(w, nx, ny, guiClass):                                # clock callback function
    w.delete(ALL)                                              # delete canvas
    guiClass.updateClock(w, nx, ny)                                        # draw clock
    w.after(5, Clock, w, nx, ny, guiClass)                  # call callback after 5 ms

# main

root = Tk()                                           # create Tk root widget
root.title("Python clock")

nx = 1000; ny = 1000                                            # canvas size
w = Canvas(root, width=nx, height=ny, bg = "white")         # create canvas w
w.pack()                                                # make canvas visible

gui = ClockGUI(combinations)

Clock(w, nx, ny, gui)                                        # call clock function
# root.after(ACTIVE_TIME, root.destroy)         # close window after given time
root.mainloop()                                    # enter Tkinter event loop
