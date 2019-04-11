from media import MediaControl
import threading
import RPi.GPIO as GPIO
import time
from subprocess import call

# TODO: implement a GPIO remote for the push button (@DavidM42 did something already)


class GpioRemote(MediaControl):

    __event = None
    __msg = None

    def __init__(self, event, msg):
        self.__event = event
        self.__msg = msg

    def __run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        counter = 0

        while True:
            input_state = GPIO.input(18)
            if input_state == False:
                counter += 1
                print('Button Pressed')
                time.sleep(0.25)
            elif counter == 1:
                self.next()
                time.sleep(0.25)
                counter = 0
            else:
                counter = 0
                time.sleep(0.25)

            if counter == 8:
                print('shutdown')
                call(["systemctl", "stop", "mpradio"])
                call(["poweroff"])
                time.sleep(1)

    def run(self):
        threading.Thread(target=self.run).start()

    def resume(self):
        pass

    def pause(self):
        pass

    def next(self):
        self.__msg["command"] = "next"
        self.__msg["source"] = "gpio"
        self.__event.set()

    def previous(self):
        pass

    def repeat(self):
        pass

    def fast_forward(self):
        pass

    def rewind(self):
        pass

    def stop(self):
        pass
