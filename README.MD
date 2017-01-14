## About Slackshot 

The purpose of this app is to record pool shots into a video and send them tho Slack
chat.  

This python app records a video using picamera. If a button is pressed, the 
last video is sent to Slack into configured channel(s).

## To run

* Install pip: `sudo apt-get install pip`
* Install pi camera: `sudo apt-get install python-picamera`
* Install slacker: `sudo pip install slacker`
* Configure api key in: `slackshot.cfg` and other config keys as you please
* python slackshot.py

## Configuration

slack.api-key -  The api key for a bot
slack.channels - Comma separated list of channels to send the videos to
slack.message - Message to post before uploading video
 
camera.width - Width of the video, e.g. 1920
camera.height - Height of the video, e.g. 1080
camera.brightness - Brightness setting for camera
camera.contrast - Contrast setting for camera
camera.frame-rate - Frame rate for video

gpio.button = GPIO pin for the button (that sends video)
gpio.pir = GPIO pin for the PIR sensor (optional)
