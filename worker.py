from strip import Strip as S
from strip import Color as C
from strip import WHITE as wht
from strip import BLUE as blue
from strip import RED as red

from vk_client import does_have_new_messages
from watch_dog import Dog
from threading import Thread

class UnreadUpdater(Thread):
    def run(self):
        self.new_messages = False
        while 1:
            try:
                self.new_messages = does_have_new_messages()
            except: pass

s = S()

u = UnreadUpdater()
u.start()

d = Dog()
d.start()

is_ambient = lambda: not d.is_available
is_alarm = lambda: u.new_messages == True and not is_ambient()
is_not_alarm = lambda: not is_alarm() and not is_ambient()

AMBIENT = red.apply_brightness(.3)

while 1:
    s.wait(AMBIENT, predicate=is_ambient)
    s.pulse(wht, red, 1.0, predicate=is_alarm)
    s.pulse(wht, wht.apply_brightness(.3), predicate=is_not_alarm)
