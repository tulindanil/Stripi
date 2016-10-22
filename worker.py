from strip import Strip as S
from strip import Color as C
from strip import WHITE as wht
from strip import BLUE as blue
from strip import RED as red

from vk_client import does_have_new_messages
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

is_alarm = lambda: u.new_messages == True
is_not_alarm = lambda: not is_alarm()

while 1:
    s.pulse(wht, red, 1.0, predicate=is_alarm)
    s.pulse(wht, wht.apply_brightness(.3), predicate=is_not_alarm)
