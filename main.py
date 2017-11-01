# File: main.py
# Purpose: driver program for the bouncing ball example

import viz
# get access to controller class
from BallZController import *

# set size (in pixels) and title of application window
viz.window.setSize( 500, 500 )
viz.window.setName( "Bouncing Ball" )

# get graphics window
window = viz.MainWindow
# setup viewing rectangle
window.ortho(-100,100,-100,100,-1,1)
# set background color of window to black 
viz.MainWindow.clearcolor( viz.BLACK ) 
# turn off mouse navigation 
viz.mouse(viz.OFF)
# center viewpoint 
viz.eyeheight(0)

# create a controller object
BallZController()

# for recording
vizact.onkeydown('b',viz.window.startRecording, 'c:\\Temp\\test.avi')
vizact.onkeydown('e',viz.window.stopRecording)
# render the scene in the window
viz.go()
