#!/usr/bin/python

# receive file from serve and save as destination
dest = 'destination'
url = 'http://www.xdowns.com/soft/xdowns2009.asp?softid=2767&downid=49&id=2767'

import socket
import os

s = socket.socket()
host = socket.gethostname()
port = 1234
s.connect(('127.0.0.1',1234))
s.send(url)

fp = open(dest,'ab')
file = s.recv(1024)

while file:
    print 'received 1kB'
    fp.write(file)
    file = s.recv(1024)
fp.close()

