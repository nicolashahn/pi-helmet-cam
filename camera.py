from picamera import PiCamera
from time import sleep
from datetime import datetime


# Constants

testing = True
resolution = (1400,1050)



with PiCamera() as camera:


	# Initialization

	camera.resolution = resolution
	timestamp = str(datetime.utcnow()).replace(' ','-').replace(':','-')
	filename = '/home/pi/cam/video/{}.h264'.format(timestamp)


	# Recording

	print 'Recording {}'.format(filename)
	if testing: camera.start_preview()
	camera.start_recording(filename)
	sleep(10)
	camera.stop_recording()
	if testing: camera.stop_preview()
