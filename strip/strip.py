import pigpio
from time import sleep

from math import sin
from math import pi

class Color(list):
    def __init__(self, *args):
        super(Color, self).__init__(args)

    def apply_brightness(self, brightness):
        return [x for x in map(lambda x: x * brightness, self)]

BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
WHITE = Color(255, 100, 50)

DEFAULT_ANIMATION_SPEED = .4

class Strip:
    def __init__(self):
        self.pi = pigpio.pi()

        self.blue_pin = 2
        self.green_pin = 3
        self.red_pin = 4

        self.pins = [4, 3, 2]

        self.test()

    def test(self):
        test_colors = [BLACK, RED, BLACK, RED, BLACK]
        for color in test_colors:
            self.sinus(color)

    def set_color(self, color):
        for pin, brightness in zip(self.pins, color):
            self.pi.set_PWM_dutycycle(pin, int(brightness))

    def get_color(self):
        return [float(self.pi.get_PWM_dutycycle(pin)) \
                for pin in self.pins]

    def animate(self, f, color, duration, blocking):
        t = .0 # that's current time
        step = .01

        initials = self.get_color()

        def calculate_value(x_1, x_2, t):
            return x_1 + f(t / duration) * (x_2 - x_1)

        def calculate_color(t):
            return map(lambda x: calculate_value(x[0], x[1], t),
                       zip(initials, color))

        while t < duration:
            self.set_color(calculate_color(t))

            t = t + step
            sleep(step)

    def straight(self, color, duration=DEFAULT_ANIMATION_SPEED, blocking=True):
        return self.animate(lambda x: x, color, duration, blocking)

    def parabola(self, color, duration=DEFAULT_ANIMATION_SPEED, blocking=True):
        return self.animate(lambda x: x ** 2, color, duration, blocking)

    def sinus(self, color, duration=DEFAULT_ANIMATION_SPEED, blocking=True):
        return self.animate(lambda x: sin(x * pi - (pi / 2)) / 2 + .5,
                            color, duration, blocking)

    def pulse(self, c_1, c_2, duration=2, interval=.5,
              predicate=lambda: True):
        while predicate():
            self.sinus(c_1, duration)
            self.sinus(c_2, duration)
