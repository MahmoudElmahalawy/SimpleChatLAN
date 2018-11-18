import socket
from _thread import *
import os
import pickle
# import sys


def threaded(s):
    while True:
        data = s.recv(1024)
        if data != bytes("{quit}", "utf8"):
            print(str(data.decode('ascii')))
        else:
            os._exit(1)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    HOST = input('Enter host: ')
    PORT = input('Enter port: ')
    if not PORT:
        PORT = 33445
    else:
        PORT = int(PORT)


    username = input('Username: ')
    password = input('Password: ')

    s.connect((HOST, PORT))
    start_new_thread(threaded, (s,))

    auth = (username, password)
    s.send(pickle.dumps(auth))
    while True:
        message = input()
        s.send(message.encode('ascii'))



main()
