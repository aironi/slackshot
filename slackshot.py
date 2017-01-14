from button import Button
import sys, getopt
import ConfigParser
import picamera
import time

from slacker import Slacker


def main(argv):
    config = ConfigParser.ConfigParser({'brightness': '50', 'contrast': '50', 'duration': '30', 'frame-rate': '30',
                                        'message': 'Check out this amazing trick-shot!', 'pir' : '-1'})
    config.read('slackshot.cfg')
    apikey = config.get('slack', 'api-key')
    if apikey is None:
        print 'Please add api-key to slackshot.cfg under [slack] -section'
        sys.exit(2)

    button_pin = config.getint('gpio', 'button')
    if button_pin is None:
        print 'Please add pin to slackshot.cfg under [button] -section'
        sys.exit(2)

    pir_pin = config.getint('gpio', 'pir')

    channels = config.get('slack', 'channels')
    slack_config = {'api-key': apikey, 'channels': channels.split(','),
                    'message': config.get('slack', 'message')}

    camera_config = {'brightness': config.getint('camera', 'brightness'),
                     'contrast': config.getint('camera', 'contrast'),
                     'duration': config.getint('camera', 'duration'),
                     'frame-rate': config.getint('camera', 'frame-rate'),
                     'resolution' : (config.getint('camera', 'width'), config.getint('camera','height'))}

    gpio_config = {'button' : button_pin, 'pir' : pir_pin}
    start_capture(slack_config, gpio_config, camera_config)


def start_capture(slack_config, gpio_config, camera_config):
    button = Button('Button', gpio_config['button'])
    pir = None
    if gpio_config['pir'] != -1:
        pir = Button('PIR sensor', gpio_config['pir'])
    else:
        print "No PIR sensor configured."

    with picamera.PiCamera() as camera:
        camera.brightness = camera_config['brightness']
        camera.contrast = camera_config['contrast']
        camera.framerate = camera_config['frame-rate']
        camera.resolution = camera_config['resolution']
        print 'Starting main loop...'
        while True:
            if pir is None or pir._pressed:
                print "Recording clip for {} seconds...".format(camera_config['duration'])
                camera.start_preview()
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

                if pir is not None:
                    pir._pressed = False

            time.sleep(0.5)

if __name__ == "__main__":
    main(sys.argv[1:])
