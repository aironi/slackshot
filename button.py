import threading
import RPi.GPIO as GPIO
import time

class Button(threading.Thread):

    _pressed = False

    def __init__(self, name, channel):
        threading.Thread.__init__(self)
        self._pressed = False
        self.channel = channel
        self.name = name
        print "Initializing channel {} as input for {}".format(self.channel, self.name)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.daemon = True
        self.start()

    def run(self):

        while True:
            current = GPIO.input(self.channel)
            time.sleep(0.2)

            if current == 1:
                self._pressed = True
                print "{} was triggered.".format(self.name)
                while self._pressed:
                    time.sleep(0.05)


