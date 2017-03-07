from picamera import PiCamera
from time import sleep
from datetime import datetime


# Constants

# to specify lines not to run during actual use
testing = True

logfile = 'videolog.log'

# (pixel width, height)
resolution = (1400,1050)

# second to film each video
interval = 10


def record(camera, filename, interval):
	""" record a single video of given length to specified file """
	if testing: print 'Recording {}'.format(filename)
	if testing: camera.start_preview()
	camera.start_recording(filename)
	sleep(interval)
	camera.stop_recording()
	if testing: camera.stop_preview()
	

def main():
	with PiCamera() as camera:


		# Initialization

		camera.resolution = resolution
		timestamp = str(datetime.utcnow()).replace(' ','-').replace(':','-')
		filename = 'video/{}.h264'.format(timestamp)

		record(camera, filename, interval)


if __name__ == "__main__":
	main()
