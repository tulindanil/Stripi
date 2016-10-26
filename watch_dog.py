from os import system
from threading import Thread
from time import sleep
from storage import Storage as S

s = S()
try:
    address = s.address()
except:
    address = input('Enter a ip-address: ')
    s.update_address(address)

class Dog(Thread):
    def run(self):
        self.is_available = False
        while 1:
            self.is_available = bool(system('ping -c ' + address))
            sleep(.5)
