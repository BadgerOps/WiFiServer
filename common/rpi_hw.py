import logging
try:
    import RPi.GPIO as gpio
except RuntimeError:
    print "Must be run on a raspberry pi"
except Exception:
    print 'cannot import the RPi.GPIO lib, is it installed?'


class RpiHW(object):

    def __init__(self):
        self.gpio_pin = 26  # FIXME: this shouldn't be here, move to cfg

    def _setup(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.gpio_pin, gpio.IN, pull_up_down=gpio.PUD_UP)


    def gpio_check(self):
            if (gpio.input(self.gpio_pin) == 0):
                return True
            else:
                return False