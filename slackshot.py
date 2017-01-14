from input import Input
from slacker import Slacker
import sys, getopt
import ConfigParser
import picamera
import time

def main(argv):
    (slack_config, camera_config, gpio_config) = parse_config()
    start_capture(slack_config, gpio_config, camera_config)

def parse_config():
    defaults = {'brightness': '50',
                'contrast': '50',
                'duration': '30',
                'frame-rate': '30',
                'message': 'Check out this amazing trick-shot!',
                'pir': '-1', # PIR is disabled by default
                'video-path' : '/home/pi/video.h264'}

    config = ConfigParser.ConfigParser(defaults)
    config.read('slackshot.cfg')
    api_key = config.get('slack', 'api-key')
    if api_key is None:
        print 'Please add api-key to slackshot.cfg under [slack] -section'
        sys.exit(2)

    button_pin = config.getint('gpio', 'button')
    if button_pin is None:
        print 'Please add button to slackshot.cfg under [gpio] -section'
        sys.exit(2)

    pir_pin = config.getint('gpio', 'pir')
    channels = config.get('slack', 'channels')
    slack_config = {'api-key': api_key, 'channels': channels.split(','),
                    'message': config.get('slack', 'message')}

    camera_config = {'video-path': config.get('camera', 'video-path'),
                     'brightness': config.getint('camera', 'brightness'),
                     'contrast': config.getint('camera', 'contrast'),
                     'duration': config.getint('camera', 'duration'),
                     'frame-rate': config.getint('camera', 'frame-rate'),
                     'resolution': (config.getint('camera', 'width'), config.getint('camera', 'height'))}

    gpio_config = {'button': button_pin, 'pir': pir_pin}

    return (slack_config, camera_config, gpio_config)


def start_capture(slack_config, gpio_config, camera_config):
    button = Input('Button', gpio_config['button'])
    pir = None
    if gpio_config['pir'] != -1:
        pir = Input('PIR sensor', gpio_config['pir'])
    else:
        print "No PIR sensor configured. Recording constantly."

    with picamera.PiCamera() as camera:
        configure_camera(camera, camera_config)
        print 'Starting main loop...'
        while True:
            if pir is None or pir._pressed:
                record_video(camera, camera_config['video-path'], camera_config['duration'])

                if pir is not None:
                    pir._pressed = False

            if button._pressed:
                send_video(slack_config, camera_config['video-path'])
                button._pressed = False

            time.sleep(0.5)


def configure_camera(camera, camera_config):
    print "Configuring camera..."
    camera.brightness = camera_config['brightness']
    camera.contrast = camera_config['contrast']
    camera.framerate = camera_config['frame-rate']
    camera.resolution = camera_config['resolution']


def record_video(camera, video_path, duration):
    print "Recording clip for {} seconds...".format(duration)
    camera.start_preview()
    camera.start_recording(video_path)
    time.sleep(duration)
    camera.stop_recording()
    camera.stop_preview()
    print "Recorded."


def send_video(slack_config, video_path):
    channels = slack_config['channels']
    message = slack_config['message']
    print "Sending video to channel(s): {}".format(channels)
    slack = Slacker(slack_config['api-key'])
    slack.chat.post_message(channels, message)
    slack.files.upload(video_path, channels=channels)

if __name__ == "__main__":
    main(sys.argv[1:])
