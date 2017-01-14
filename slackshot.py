import sys, getopt
import ConfigParser

import picamera
import time
from slacker import Slacker

def main(argv):
    config = ConfigParser.ConfigParser()
    config.read('slackshot.cfg')
    apikey = config.get('config', 'api-key')
    if apikey is None:
         print 'Please add api-key to slackshot.cfg under [config] -section'
         sys.exit(2)

    start_capture(apikey)


def start_capture(apikey):
    # add loop
    with picamera.PiCamera() as camera:
        camera.start_preview()

        time.sleep(3)

        camera.capture('/home/pi/image.jpg')

        camera.stop_preview()

        slack = Slacker(apikey)
        slack.chat.post_message('#slackshot-test', 'Check out this amazing trick-shot!')
        slack.files.upload('/home/pi/image.jpg', channels="slackshot-test")


if __name__ == "__main__":
    main(sys.argv[1:])