#!/usr/bin/python

# run server, a file named source will be read and sent to client
source = 'source'

import socket
import os

s = socket.socket()
host = socket.gethostname()
port = 1234
s.bind((host,port))
s.listen(5)

fp = open(source,'rb')
file = fp.read()
fp.close()
while True:
    c,addr=s.accept()
    print 'Got connection from',addr
    c.send(file)
    c.close()
