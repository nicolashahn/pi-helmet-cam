# pi-helmet-cam
# recording script for a Raspberry Pi powered motorcycle helmet camera
# Nicolas Hahn

import os
from time import sleep
from datetime import datetime
from shutil import rmtree
from sys import exit, argv
from subprocess import Popen, PIPE
from picamera import PiCamera

# to specify lines not to run during actual use
debug = False

videodir = 'video'
filetype = 'h264'

# how many 0s to put in front of counter number
# will start to screw up when video has passed (interval)*10^(zfill_decimal) seconds in length
zfill_decimal = 6 

# 8mp V2 camera
resolution = (1640, 1232)
framerate = 30

# number of seconds to film each video
interval = 5

# check for enough disk space every (this many) of above intervals
space_check_interval = 100

# what % of disk space must be free to start a new video
required_free_space_percent = 15 # about an hour with 64gb card

# start a new video after current reaches this size
max_video_size = 5000 * (10 ** 6)  # ~45 minutes

class OutputShard(object):
    def __init__(self, filename):
        self.filename = filename
        self.is_new = self.size == 0
        self.stream = open(filename, 'ab')

    def __repr__(self):
        return '<OutputShard:%s>' % self.filename

    def write(self, buf):
        self.stream.write(buf)

    def close(self):
        self.stream.close()

    def remove(self):
        os.remove(self.filename)

    @property
    def size(self):
        try:
            return os.stat(self.filename).st_size
        except OSError:
            return 0

def make_room(videodir):
    """ clear oldest video """
    sorted_videos = sorted(os.listdir(videodir))
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
    """ true if disk is (given percent)% free """
    df = Popen(["df", "/"], stdout=PIPE)
    output = df.communicate()[0]
    percent_used_str = output.split("\n")[1].split()[4]
    percent_used = int(percent_used_str.replace('%',''))
    if debug: print '{}% of disk space used.'.format(percent_used)
    enough = 100 >= required_free_space_percent + percent_used
    if debug: print 'Enough space to start new video: {}'.format(enough)
    return enough

def generate_filename(videodir, timestamp, counter):
    """ going to look like: 2017-03-08-09-54-27.334326-000001.h264 """
    filename_prefix = '{}/{}'.format(videodir, timestamp)
    if not os.path.isdir(filename_prefix):
        if debug: print 'Creating directory {}'.format(filename_prefix)
        os.mkdir(filename_prefix)
    zfill_counter = str(counter).zfill(zfill_decimal)
    filename =  '{}/{}-{}.{}'.format(filename_prefix, timestamp, zfill_counter, filetype)
    if debug: print 'Recording {}'.format(filename)
    return filename

def continuous_record(camera, videodir, interval):
    """ record <interval> second files with prefix """
    timestamp = str(datetime.now()).replace(' ','-').replace(':','-')
    if debug: camera.start_preview()
    counter = 0 # number of video files created
    intervals_recorded = 0 # number of time intervals recorded
    shard = OutputShard(generate_filename(videodir, timestamp, counter))
    camera.start_recording(shard, format=filetype, intra_period=interval*framerate)
    while(True):
        intervals_recorded += 1
        camera.split_recording(shard)
        camera.wait_recording(interval)
        if shard.size > max_video_size:
            counter += 1
        if counter % space_check_interval == 0:
            while not enough_disk_space(required_free_space_percent):
                make_room(videodir)
        shard = OutputShard(generate_filename(videodir, timestamp, counter))
    camera.stop_recording()
    if debug: camera.stop_preview()

def main():
    with PiCamera() as camera:
        # Initialization
        camera.resolution = resolution
        camera.framerate = framerate
        while not enough_disk_space(required_free_space_percent):
            make_room(videodir)
        # start recording, chunking files every <interval> seconds
        continuous_record(camera, videodir, interval)

if __name__ == "__main__":
    if len(argv) > 1:
        if argv[1] in ('-d', '--debug'):
            debug = True
    main()
