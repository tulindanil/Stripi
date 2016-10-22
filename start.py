from os import fork, system

if fork() == 0:
    system('python3 worker.py')
