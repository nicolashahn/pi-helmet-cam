from picamera import PiCamera
from time import sleep
from datetime import datetime
from os import mkdir
from os.path import isdir
import sys
import subprocess

# Constants

# to specify lines not to run during actual use
testing = False

videodir = 'video'
logfile = 'videolog.log' #TODO
filetype = 'h264'

# how many 0s to put in front of counter number
# will start to screw up when video has passed (interval)*10^(zfill_decimal) seconds in length
zfill_decimal = 6 

# (pixel width, height)
resolution = (1296, 972)
framerate = 30

# number of seconds to film each video
interval = 5

# what % of disk space must be free to start a new video
required_free_space_percent = 10

def enough_disk_space():
	""" return true if we have enough space to start a new video """
	df = subprocess.Popen(["df", "/"], stdout=subprocess.PIPE)
	output = df.communicate()[0]
	percent_str = output.split("\n")[1].split()[4]
	percent_used = int(percent_str.replace('%',''))
	if testing: print '{}% of disk space used.'.format(percent_used)
	enough = 100 >= required_free_space_percent + percent_used
	if testing: print 'Enough space to start new video: {}'.format(enough)
	return enough


def generate_filename(videodir, timestamp, counter, filetype):
	filename_prefix = '{}/{}'.format(videodir, timestamp)
	if not isdir(filename_prefix):
		if testing: print 'Creating directory {}'.format(filename_prefix)
		mkdir(filename_prefix)
	zfill_counter = str(counter).zfill(zfill_decimal)
	filename =  "{}/{}-{}.{}".format(filename_prefix, timestamp, zfill_counter, filetype)
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
		camera.framerate = framerate
		timestamp = str(datetime.now()).replace(' ','-').replace(':','-')
		enough_disk_space()

		# start recording, chunking files every <interval> seconds
		continuous_record(camera, videodir, timestamp, filetype, interval)


if __name__ == "__main__":
	if len(sys.argv) > 1:
		if sys.argv[1] == '-t' or sys.argv[1] == '--testing':
			testing = True
	main()
