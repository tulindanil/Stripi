from strip import Strip as S
from strip import Color as C
from strip import WHITE as wht
from strip import BLUE as blue
from strip import RED as red

from vk_client import does_have_new_messages
from threading import Thread

class UnreadUpdater(Thread):
    def __init__(self, *args):
        self.new_messages = False
        super(Thread, self).__init__(args)

    def run(self):
        try:
            self.new_messages = does_have_new_messages()

s = S()

u = UnreadUpdater()
u.start()

is_alarm = lambda: u.new_messages == True
is_not_alarm = lambda: now is_alarm()

while 1:
    if is_alarm():
        s.pulse(wht, red, 1.0, predicate=is_alarm)
    else:
        s.pulse(wht, wht.apply_brightness(.3), predicate=is_not_alarm)
