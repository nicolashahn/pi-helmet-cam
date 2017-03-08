# pi-helmet-cam
Software for a Raspberry Pi Zero W motorcycle helmet camera

## Necessary Hardware

- Raspberry Pi
  - Zero/Zero Wireless ideally
- Raspberry Pi camera 
  - an offical Raspberry Pi camera is a safe bet
  - with correct ribbon cable (Zero cable is different than full sized Pi's, also should get at least 6" long)
- MicroSD card
  - get one of the 'high endurance' ones since this will be writing HD video constantly
- Battery
  - Simplest solution is a smartphone external battery pack with a microUSB cable, and just keep it in your jacket
- Camera housing/mounting
  - I made mine out of plexiglass, superglue, and electrical tape for waterproofing with a dremel
  - Electrical tape or double sided adhesive pads for mounting camera+Pi to the helmet
- You might also need for setup/troubleshooting
  - Monitor/TV
  - USB keyboard
  - Adapter for mini HDMI -> HDMI or whatever your monitor/TV takes
  - Adapter for microUSB -> USB for a keyboard so you can set up Raspbian

## Setup Instructions

// TODO not finished

#### Set up your Raspberry Pi and camera

I used a Raspberry Pi Zero Wireless, but any that can interface with a Raspberry Pi camera will work. I'll leave it to other online guides to show you how to get it set up. I'm also going to assume if you're trying this you have a working knowledge of Unix, shell scripting, and Python.

Get your Pi set up with a camera (I used an Arducam 5mp, a $17 knockoff of the 1st gen Raspberry Pi official camera) and Raspbian installed and camera enabled via `raspi-config`, then `git clone` this repository into your `~` directory.

#### cronjob for recording on boot up:

(run `sudo crontab -e` and add this line to the bottom)

    @reboot sh /home/pi/pi-helmet-cam/boot_script.sh >/home/pi/pi-helmet-cam/cronlog 2>&1

- NOTE: depending on what your username is/where you put this repo you may need to change the path
- If you're running into problems starting the script on boot, check `./cronlog`.


## Files

#### `camera.py`

- Python script that begins recording video in chunks when started
- Use `-t` or `--testing` to see video preview

#### `boot_script.sh`

- clears out old videos if we need the space
- then starts recording
- crontab runs this on startup

#### `clear_videos.sh`

- helpful script to just clean out old video from the `video` directory

#### `video/`
- the Python script will create a `video` directory to store videos in
- each video will have its own directory, the name being a current timestamp
- inside this, there will be 5 second clips with the form `<timestamp>-000001.h264`
- protip: when you move this directory to your laptop/desktop, you can select all files and open them with VLC or similar and they'll play in order
- TODO: have script automatically merge the files after recording

#### `cronlog`
- where logs from starting the script on boot with `cronjob` will go
