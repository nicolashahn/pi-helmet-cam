# pi-helmet-cam
# recording script for a Raspberry Pi powered motorcycle helmet camera
# Nicolas Hahn

from picamera import PiCamera
from time import sleep
from datetime import datetime
from os import mkdir, listdir
from os.path import isdir
from shutil import rmtree
from sys import exit, argv
from subprocess import Popen, PIPE



# to specify lines not to run during actual use
debug = False

videodir = 'video'
filetype = 'h264'

# how many 0s to put in front of counter number
# will start to screw up when video has passed (interval)*10^(zfill_decimal) seconds in length
zfill_decimal = 6 

# best settings for 5mp V1 camera
# (pixel width, height)
# resolution = (1296, 972)
# framerate = 30

# 8mp V2 camera
resolution = (1640, 1232)
framerate = 30

# number of seconds to film each video
interval = 5

# check for enough disk space every (this many) of above intervals
space_check_interval = 100

# what % of disk space must be free to start a new video
required_free_space_percent = 15 # about an hour



def make_room(videodir):
	""" clear oldest video """
	sorted_videos = sorted(listdir(videodir))
	if sorted_videos:
		oldest_video = sorted_videos[0]
		if debug: print 'Removing oldest video: {}'.format(oldest_video)
		# may not have permission if running as pi and video was created by root
	try:
			rmtree('{}/{}'.format(videodir, oldest_video)) 
		except OSError as e:
			print 'ERROR, must run as root otherwise script cannot clear out old videos'
			exit(1)
	else:
		if debug: print 'No videos in directory {}, cannot make room'.format(videodir)


def enough_disk_space(required_free_space_percent):
	""" return true if we have enough space to start a new video """
	df = Popen(["df", "/"], stdout=PIPE)
	output = df.communicate()[0]
	percent_used_str = output.split("\n")[1].split()[4]
	percent_used = int(percent_used_str.replace('%',''))
	if debug: print '{}% of disk space used.'.format(percent_used)
	enough = 100 >= required_free_space_percent + percent_used
	if debug: print 'Enough space to start new video: {}'.format(enough)
	return enough


def generate_filename(videodir, timestamp, counter, filetype):
	""" going to look like: 2017-03-08-09-54-27.334326-000001.h264 """
	filename_prefix = '{}/{}'.format(videodir, timestamp)
	if not isdir(filename_prefix):
		if debug: print 'Creating directory {}'.format(filename_prefix)
		mkdir(filename_prefix)
	zfill_counter = str(counter).zfill(zfill_decimal)
	filename =  '{}/{}-{}.{}'.format(filename_prefix, timestamp, zfill_counter, filetype)
	if debug: print 'Recording {}'.format(filename)
	return filename


def continuous_record(camera, videodir, timestamp, filetype, interval):
	""" record <interval> second files with prefix """
	counter = 0
	if debug: camera.start_preview()
	initial_filename = generate_filename(videodir, timestamp, counter, filetype)
	camera.start_recording(initial_filename)
	camera.wait_recording(interval)
	while(True):
		counter += 1
		split_filename = generate_filename(videodir, timestamp, counter, filetype)
		camera.split_recording(split_filename)
		camera.wait_recording(interval)
		if counter % space_check_interval == 0:
			while not enough_disk_space(required_free_space_percent):
				make_room(videodir)
	camera.stop_recording()
	if debug: camera.stop_preview()
	

def main():
	with PiCamera() as camera:

		# Initialization
		camera.resolution = resolution
		camera.framerate = framerate
		timestamp = str(datetime.now()).replace(' ','-').replace(':','-')
		while not enough_disk_space(required_free_space_percent):
			make_room(videodir)

		# start recording, chunking files every <interval> seconds
		continuous_record(camera, videodir, timestamp, filetype, interval)


if __name__ == "__main__":
	if len(argv) > 1:
		if argv[1] == '-d' or argv[1] == '--debug':
			debug = True
	main()
