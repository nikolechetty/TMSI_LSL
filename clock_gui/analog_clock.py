# Analog clock with callback function
from tkinter import *                                 # import Tkinter module
from math import *
from time import *
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

def Clock0(w, nx, ny):                                  # clock draw function
   x0 = nx/2; lx = 9*nx/20              # center and half-width of clock face
   y0 = ny/2; ly = 9*ny/20
   r0 = 0.9 * min(lx,ly)                # distance of hour labels from center
   r1 = 0.6 * min(lx,ly)                                # length of hour hand
   r2 = 0.8 * min(lx,ly)                              # length of minute hand

   w.create_oval(x0-lx, y0-ly, x0+lx, y0+ly, width=2)            # clock face
#    for i in range(1,13):                               # label the clock face
#       phi = pi/6 * i                              # angular position of label
#       x = x0 + r0 * sin(phi)                    # Cartesian position of label
#       y = y0 - r0 * cos(phi)
#       w.create_text(x, y, text=str(i))                           # hour label

   w.create_arc(x0-lx, y0-ly, x0+lx, y0+ly, start=290, extent=20, style=PIESLICE, fill="blue")

   t = localtime()                                             # current time
   t_s = t[5]                                                       # seconds
   t_m = t[4] + t_s/60                                              # minutes
   t_h = t[3] % 12 + t_m/60                                    # hours [0,12]

#    phi = pi/6 * t_h                                         # hour hand angle
#    x = x0 + r1 * sin(phi)                             # position of arrowhead
#    y = y0 - r1 * cos(phi)                                    # draw hour hand
#    w.create_line(x0, y0, x, y, arrow=LAST, fill="red", width=6)

#    phi = pi/30 * t_m                                      # minute hand angle
#    x = x0 + r2 * sin(phi)                             # position of arrowhead
#    y = y0 - r2 * cos(phi)                                  # draw minute hand
#    w.create_line(x0, y0, x, y, arrow=LAST, fill="blue", width=4)

   phi = pi/30 * t_s                                      # second hand angle
   x = x0 + r2 * sin(phi)                             # position of arrowhead
   y = y0 - r2 * cos(phi)
   w.create_line(x0, y0 , x, y, arrow=LAST, width=2)                # draw second hand

def Clock(w, nx, ny):                               # clock callback function
   w.delete(ALL)                                              # delete canvas
   Clock0(w, nx, ny)                                             # draw clock
   w.after(10, Clock, w, nx, ny)                  # call callback after 10 ms

# main

root = Tk()                                           # create Tk root widget
root.title("Python clock")

nx = 1000; ny = 1000                                              # canvas size
w = Canvas(root, width=nx, height=ny, bg = "white")         # create canvas w
w.pack()                                                # make canvas visible

Clock(w, nx, ny)                                        # call clock function

root.mainloop()                                    # enter Tkinter event loop



# try:
# 	import Tkinter
# except:
# 	import tkinter as Tkinter

# import math	# Required For Coordinates Calculation
# import time	# Required For Time Handling
# #
# #
# # class
# class main(Tkinter.Tk):
# 	def __init__(self):
# 		Tkinter.Tk.__init__(self)
# 		self.x=150	# Center Point x
# 		self.y=150	# Center Point
# 		self.length=50	# Stick Length
# 		self.creating_all_function_trigger()

# 	# Creating Trigger For Other Functions
# 	def creating_all_function_trigger(self):
# 		self.create_canvas_for_shapes()
# 		self.creating_background_()
# 		self.creating_sticks()
# 		return

# 	# Creating Background
# 	def creating_background_(self):
# 		self.image=Tkinter.PhotoImage(file='clock.gif')
# 		self.canvas.create_image(150,150, image=self.image)
# 		return

# 	# creating Canvas
# 	def create_canvas_for_shapes(self):
# 		self.canvas=Tkinter.Canvas(self, bg='black')
# 		self.canvas.pack(expand='yes',fill='both')
# 		return

# 	# Creating Moving Sticks
# 	def creating_sticks(self):
# 		self.sticks=[]
# 		for i in range(3):
# 			store=self.canvas.create_line(self.x, self.y,self.x+self.length,self.y+self.length,width=2, fill='red')
# 			self.sticks.append(store)
# 		return

# 	# Function Need Regular Update
# 	def update_class(self):
# 		now=time.localtime()
# 		t = time.strptime(str(now.tm_hour), "%H")
# 		hour = int(time.strftime( "%I", t ))*5
# 		now=(hour,now.tm_min,now.tm_sec)
# 		# Changing Stick Coordinates
# 		for n,i in enumerate(now):
# 			x,y=self.canvas.coords(self.sticks[n])[0:2]
# 			cr=[x,y]
# 			cr.append(self.length*math.cos(math.radians(i*6)-math.radians(90))+self.x)
# 			cr.append(self.length*math.sin(math.radians(i*6)-math.radians(90))+self.y)
# 			self.canvas.coords(self.sticks[n], tuple(cr))
# 		return

# # Main Function Trigger
# if __name__ == '__main__':
# 	root=main()

# 	# Creating Main Loop
# 	while True:
# 		root.update()
# 		root.update_idletasks()
# 		root.update_class()

# ###############################################################################
# # PyClock: a clock GUI, with both analog and digital display modes, a 
# # popup date label, clock face images, resizing, etc. May be run both 
# # stand-alone, or embbeded (attached) in other GUIs that need a clock.
# ###############################################################################

# from tkinter import *
# import math, time, string, sys


# ###############################################################################
# # Option configuration classes
# ###############################################################################


# class ClockConfig: 
#     # defaults--override in instance or subclass
#     size = 200 # width=height
#     bg, fg = 'beige', 'brown' # face, tick colors
#     hh, mh, sh, cog = 'black', 'navy', 'blue', 'red' # clock hands, center
#     picture = None # face photo file

# class PhotoClockConfig(ClockConfig): 
#     # sample configuration
#     size = 320
#     picture = '../gifs/ora-pp.gif'
#     bg, hh, mh = 'white', 'blue', 'orange'


# ###############################################################################
# # Digital display object
# ###############################################################################

# class DigitalDisplay(Frame):
#     def __init__(self, parent, cfg):
#         Frame.__init__(self, parent)
#         self.hour = Label(self)
#         self.mins = Label(self)
#         self.secs = Label(self)
#         self.ampm = Label(self)
#         for label in self.hour, self.mins, self.secs, self.ampm:
#             label.config(bd=4, relief=SUNKEN, bg=cfg.bg, fg=cfg.fg)
#             label.pack(side=LEFT)

#     def onUpdate(self, hour, mins, secs, ampm, cfg):
#         mins = string.zfill(str(mins), 2)
#         self.hour.config(text=str(hour), width=4) 
#         self.mins.config(text=str(mins), width=4) 
#         self.secs.config(text=str(secs), width=4) 
#         self.ampm.config(text=str(ampm), width=4) 

#     def onResize(self, newWidth, newHeight, cfg): 
#         pass # nothing to redraw here


# ###############################################################################
# # Analog display object
# ###############################################################################

# class AnalogDisplay(Canvas):
#     def __init__(self, parent, cfg):
#         Canvas.__init__(self, parent, 
#         width=cfg.size, height=cfg.size, bg=cfg.bg)
#         self.drawClockface(cfg)
#         self.hourHand = self.minsHand = self.secsHand = self.cog = None 

#     def drawClockface(self, cfg): # on start and resize 
#         if cfg.picture: # draw ovals, picture
#             try:
#                 self.image = PhotoImage(file=cfg.picture) # bkground
#             except:
#                 self.image = BitmapImage(file=cfg.picture) # save ref
#                 imgx = (cfg.size - self.image.width( )) / 2 # center it
#                 imgy = (cfg.size - self.image.height( )) / 2
#                 self.create_image(imgx+1, imgy+1, anchor=NW, image=self.image) 
#                 originX = originY = radius = cfg.size/2
#                 for i in range(60):
#                     x, y = self.point(i, 60, radius-6, originX, originY)
#                     self.create_rectangle(x-1, y-1, x+1, y+1, fill=cfg.fg) # mins
#                 for i in range(12):
#                     x, y = self.point(i, 12, radius-6, originX, originY)
#                     self.create_rectangle(x-3, y-3, x+3, y+3, fill=cfg.fg) # hours
#                     self.ampm = self.create_text(3, 3, anchor=NW, fill=cfg.fg)

#     def point(self, tick, units, radius, originX, originY):
#         angle = tick * (360.0 / units)
#         radiansPerDegree = math.pi / 180
#         pointX = int( round( radius * math.sin(angle * radiansPerDegree) )) 
#         pointY = int( round( radius * math.cos(angle * radiansPerDegree) ))
#         return (pointX + originX+1), (originY+1 - pointY)

#     def onUpdate(self, hour, mins, secs, ampm, cfg): # on timer callback
#         if self.cog: # redraw hands, cog
#             self.delete(self.cog) 
#             self.delete(self.hourHand)
#             self.delete(self.minsHand)
#             self.delete(self.secsHand)
#             originX = originY = radius = cfg.size/2
#             hour = hour + (mins / 60.0)
#             hx, hy = self.point(hour, 12, (radius * .80), originX, originY)
#             mx, my = self.point(mins, 60, (radius * .90), originX, originY)
#             sx, sy = self.point(secs, 60, (radius * .95), originX, originY)
#             self.hourHand = self.create_line(originX, originY, hx, hy, 
#             width=(cfg.size * .04),
#             arrow='last', arrowshape=(25,25,15), fill=cfg.hh)
#             self.minsHand = self.create_line(originX, originY, mx, my, 
#             width=(cfg.size * .03),
#             arrow='last', arrowshape=(20,20,10), fill=cfg.mh)
#             self.secsHand = self.create_line(originX, originY, sx, sy, 
#             width=1,
#             arrow='last', arrowshape=(5,10,5), fill=cfg.sh)
#             cogsz = cfg.size * .01
#             self.cog = self.create_oval(originX-cogsz, originY+cogsz, 
#             originX+cogsz, originY-cogsz, fill=cfg.cog)
#             self.dchars(self.ampm, 0, END)
#             self.insert(self.ampm, END, ampm)

#     def onResize(self, newWidth, newHeight, cfg):
#         newSize = min(newWidth, newHeight)
#         #print 'analog onResize', cfg.size+4, newSize
#         if newSize != cfg.size+4:
#             cfg.size = newSize-4
#             self.delete('all')
#             self.drawClockface(cfg) # onUpdate called next


# ###############################################################################
# # Clock composite object
# ###############################################################################

# ChecksPerSec = 10 # second change timer

# class Clock(Frame):
#     def __init__(self, config=ClockConfig, parent=None):
#         Frame.__init__(self, parent)
#         self.cfg = config
#         self.makeWidgets(parent) # children are packed but
#         self.labelOn = 0 # clients pack or grid me
#         self.display = self.digitalDisplay
#         self.lastSec = -1
#         self.onSwitchMode(None)
#         self.onTimer( )

#     def makeWidgets(self, parent):
#         self.digitalDisplay = DigitalDisplay(self, self.cfg)
#         self.analogDisplay = AnalogDisplay(self, self.cfg)
#         self.dateLabel = Label(self, bd=3, bg='red', fg='blue')
#         parent.bind('', self.onSwitchMode)
#         parent.bind('', self.onToggleLabel)
#         parent.bind('', self.onResize)

#     def onSwitchMode(self, event):
#         self.display.pack_forget( )
#         if self.display == self.analogDisplay:
#             self.display = self.digitalDisplay
#         else:
#             self.display = self.analogDisplay
#             self.display.pack(side=TOP, expand=YES, fill=BOTH)

#     def onToggleLabel(self, event):
#         self.labelOn = self.labelOn + 1
#         if self.labelOn % 2:
#             self.dateLabel.pack(side=BOTTOM, fill=X)
#         else:
#             self.dateLabel.pack_forget( )
#         self.update( )

#     def onResize(self, event):
#         if event.widget == self.display:
#             self.display.onResize(event.width, event.height, self.cfg)

#     def onTimer(self):
#         secsSinceEpoch = time.time( ) 
#         timeTuple = time.localtime(secsSinceEpoch) 
#         hour, min, sec = timeTuple[3:6] 
#         if sec != self.lastSec:
#             self.lastSec = sec
#         ampm = ((hour >= 12) and 'PM') or 'AM' # 0...23
#         hour = (hour % 12) or 12 # 12..11
#         self.display.onUpdate(hour, min, sec, ampm, self.cfg)
#         self.dateLabel.config(text=time.ctime(secsSinceEpoch))
#         self.after(1000 / ChecksPerSec, self.onTimer) # run N times per second


# ###############################################################################
# # Stand-alone clocks
# ###############################################################################

# class ClockWindow(Clock):
#     def __init__(self, config=ClockConfig, parent=None, name=''):
#         Clock.__init__(self, config, parent)
#         self.pack(expand=YES, fill=BOTH)
#         title = 'PyClock 1.0' 
#         if name: title = title + ' - ' + name
#         self.master.title(title) # master=parent or default
#         self.master.protocol('WM_DELETE_WINDOW', self.quit) 


# ###############################################################################
# # Program run
# ###############################################################################

# if __name__ == '__main__': 
#     def getOptions(config, argv):
#         for attr in dir(ClockConfig): # fill default config obj,
#             try: # from "-attr val" cmd args
#                 ix = argv.index('-' + attr)
#             except:
#                 continue
#             else:
#                 if ix in range(1, len(argv)-1):
#                     if type(getattr(ClockConfig, attr)) == type(0):
#                         setattr(config, attr, int(argv[ix+1]))
#                     else:
#                         setattr(config, attr, argv[ix+1]) 
            
#     config = ClockConfig( ) 
#     #config = PhotoClockConfig( )
#     if len(sys.argv) >= 2:
#         getOptions(config, sys.argv) # clock.py -size n -bg 'blue'...
#     myclock = ClockWindow(config, Tk( )) # parent is Tk root if standalone
#     myclock.mainloop( )

