from os import fork, system

if fork() == 0:
    system('sudo python3 worker.py')
