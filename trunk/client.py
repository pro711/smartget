#!/usr/bin/python

# receive file from serve and save as destination
dest = 'destination'

import socket
import os

s = socket.socket()
host = socket.gethostname()
port = 1234
s.connect(('127.0.0.1',1234))
fp = open(dest,'ab')
fp.write(s.recv(1024))
file = s.recv(1024)
while file:
    fp.write(file)
    file = s.recv(1024)
fp.close()
