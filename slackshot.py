import sys, getopt
import picamera
import time
from slacker import Slacker

def main(argv):
    apikey = ''
    try:
        opts, args = getopt.getopt(argv,"hk:o:",["apikey="])
    except getopt.GetoptError:
        print 'slackshot.py -k <slack api key'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'slackshot.py -k <slack api key>'
            sys.exit()
        elif opt in ("-k", "--key"):
            apikey = arg

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

        # Upload a file
        slack.files.upload('/home/pi/image.jpg', channels="slackshot-test")
        #slack.files.upload('/home/pi/image.jpg')

if __name__ == "__main__":
    main(sys.argv[1:])