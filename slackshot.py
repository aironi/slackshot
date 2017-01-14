import sys, getopt
import ConfigParser

import picamera
import time
from slacker import Slacker

def main(argv):
    config = ConfigParser.ConfigParser({'brightness' : '50', 'contrast' : '50'})
    config.read('slackshot.cfg')
    apikey = config.get('slack', 'api-key')
    if apikey is None:
         print 'Please add api-key to slackshot.cfg under [slack] -section'
         sys.exit(2)

    brightness = config.getint('camera', 'brightness')
    contrast = config.getint('camera', 'contrast')
    camera_config = { 'brightness' : brightness, 'contrast' : contrast }
    start_capture(apikey, camera_config)


def start_capture(apikey, camera_config):
    # add loop
    with picamera.PiCamera() as camera:
        camera.brightness = camera_config['brightness']
        camera.contrast = camera_config['contrast']

        camera.start_preview()

        time.sleep(3)

        camera.capture('/home/pi/image.jpg')

        camera.stop_preview()

        slack = Slacker(apikey)
        slack.chat.post_message('#slackshot-test', 'Check out this amazing trick-shot!')
        slack.files.upload('/home/pi/image.jpg', channels="slackshot-test")


if __name__ == "__main__":
    main(sys.argv[1:])