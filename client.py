#!/usr/bin/python

# receive file from serve and save as destination
dest = 'destination'
url = 'http://www.xdowns.com/soft/xdowns2009.asp?softid=2767&downid=49&id=2767'
MAXBUFFER = 1048576

import socket
import os


s = socket.socket()
host = socket.gethostname()
port = 1234
s.connect(('127.0.0.1',1234))

request = url + '\n' + str(0) + '\n' + str(0)

s.send(request)

fp = open(dest,'ab')
file = s.recv(1024)
buffer = ''
while file:
    print 'received 16kB'
    buffer += file
    if buffer >= MAXBUFFER:
        fp.write(file)
        buffer = ''
    file = s.recv(16384)
fp.close()

