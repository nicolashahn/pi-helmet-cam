from picamera import PiCamera
from time import sleep
from datetime import datetime
from os import mkdir
from os.path import isdir


# Constants

# to specify lines not to run during actual use
testing = True

videodir = 'video'
logfile = 'videolog.log'
filetype = 'h264'

# (pixel width, height)
resolution = (1400,1050)

# number of seconds to film each video
interval = 5


def generate_filename(videodir, timestamp, counter, filetype):
	filename_prefix = '{}/{}'.format(videodir, timestamp)
	if not isdir(filename_prefix):
		if testing: print 'Creating directory {}'.format(filename_prefix)
		mkdir(filename_prefix)
	filename =  "{}/{}-{}.{}".format(filename_prefix, timestamp, counter, filetype)
	if testing: print 'Recording {}'.format(filename)
	return filename


def continuous_record(camera, videodir, timestamp, filetype, interval):
	""" record <interval> second files with prefix """
	counter = 0
	if testing: camera.start_preview()
	initial_filename = generate_filename(videodir, timestamp, counter, filetype)
	camera.start_recording(initial_filename)
	camera.wait_recording(interval)
	while(True):
		counter += 1
		split_filename = generate_filename(videodir, timestamp, counter, filetype)
		camera.split_recording(split_filename)
		camera.wait_recording(interval)
	camera.stop_recording()
	if testing: camera.stop_preview()
	

def main():
	with PiCamera() as camera:

		# Initialization
		camera.resolution = resolution
		timestamp = str(datetime.utcnow()).replace(' ','-').replace(':','-')

		# start recording, chunking files every <interval> seconds
		continuous_record(camera, videodir, timestamp, filetype, interval)


if __name__ == "__main__":
	main()
