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

#### Set up Raspberry Pi, camera, and mounting

Found in the main Google Doc for this project: https://docs.google.com/document/d/1HNO4g3zqxcsHzVkxqeB1x39abU7UEovlvAk7Gv2QWl4/edit?usp=sharing

#### cronjob for recording on boot up:

(run `sudo crontab -e` and add this line to the bottom)

    @reboot sh /home/pi/pi-helmet-cam/boot_script.sh >/home/pi/pi-helmet-cam/cronlog 2>&1

- NOTE: depending on what your username is/where you put this repo you may need to change the path
- If you're running into problems starting the script on boot, check `./cronlog`.


## Files

#### `camera.py`

- Python script that begins recording video in chunks when started
- Use `-t` or `--testing` to see video preview and/or debug print statements

#### `boot_script.sh`

- clears out old videos if we need the space
- then starts recording
- crontab runs this on startup

#### `clear_videos.sh`

- helpful script to just clean out old video from the `video` directory

#### `kill_process.sh`

- kill all running python processes, quick way to stop the script if running in background

#### `video/`
- the Python script will create a `video` directory to store videos in
- each video will have its own directory, the name being a current timestamp
- inside this, there will be 5 second clips with the form `<timestamp>-000001.h264`
- protip: when you move this directory to your laptop/desktop, you can select all files and open them with VLC or similar and they'll play in order
- TODO: have script automatically merge the files after recording

#### `cronlog`
- where logs from starting the script on boot with `cronjob` will go
