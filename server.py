#!/usr/bin/python

# run server, a file named source will be read and sent to client
source = 'source'

import socket
import os
from download import downloadurl

s = socket.socket()
host = socket.gethostname()
port = 1234
s.bind((host,port))
s.listen(5)

# fp = open(source,'rb')
# file = fp.read()
# fp.close()
while True:
    c,addr=s.accept()
    print 'Got connection from',addr
    url = c.recv(1024)
    print 'Got url'+url
    c.send(downloadurl(url))
    c.close()
