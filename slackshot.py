from button import Button
import sys, getopt
import ConfigParser
import picamera
import time

from slacker import Slacker


def main(argv):
    config = ConfigParser.ConfigParser({'brightness': '50', 'contrast': '50', 'duration': '30', 'frame-rate': '30',
                                        'message': 'Check out this amazing trick-shot!'})
    config.read('slackshot.cfg')
    apikey = config.get('slack', 'api-key')
    if apikey is None:
        print 'Please add api-key to slackshot.cfg under [slack] -section'
        sys.exit(2)

    button_pin = config.getint('button', 'pin')
    if button_pin is None:
        print 'Please add pin to slackshot.cfg under [button] -section'
        sys.exit(2)

    channels = config.get('slack', 'channels')
    slack_config = {'api-key': apikey, 'channels': channels.split(','),
                    'message': config.get('slack', 'message')}

    camera_config = {'brightness': config.getint('camera', 'brightness'),
                     'contrast': config.getint('camera', 'contrast'),
                     'duration': config.getint('camera', 'duration'),
                     'frame-rate': config.getint('camera', 'frame-rate'),
                     'resolution' : (config.getint('camera', 'width'), config.getint('camera','height'))}

    start_capture(slack_config, button_pin, camera_config)


def start_capture(slack_config, button_pin, camera_config):
    button = Button(button_pin)

    with picamera.PiCamera() as camera:
        camera.brightness = camera_config['brightness']
        camera.contrast = camera_config['contrast']
        camera.framerate = camera_config['frame-rate']
        camera.resolution = camera_config['resolution']
        print 'Starting recording loop...'
        while True:
            camera.start_preview()
            print "Recording clip..."
            camera.start_recording('/home/pi/video.h264')
            time.sleep(camera_config['duration'])
            camera.stop_recording()

            camera.stop_preview()

            if button._pressed:
                channels = slack_config['channels']
                message = slack_config['message']
                print "Sending video to channel(s): {}".format(channels)
                slack = Slacker(slack_config['api-key'])
                slack.chat.post_message(channels, message)
                slack.files.upload('/home/pi/video.h264', channels=channels)
                button._pressed = False
            else:
                print "No button press detected."

            time.sleep(0.5)

if __name__ == "__main__":
    main(sys.argv[1:])
