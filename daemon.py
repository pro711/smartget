#!/usr/bin/python

# run server, a file named source will be read and sent to client
source = 'source'

import socket
import os
from download import MyURLopener

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

    request_list = c.recv(1024).split('\n')
    print 'Got request:\nURL:'+request_list[0]+'\nStart:'+request_list[1]+'\nEnd:'+request_list[2]

    opener = MyURLopener()
    opener.openurl(request_list[0],request_list[1],request_list[2])

    data = opener.sock.read(16384)
    while data:
        c.send(data)
        data = opener.sock.read(16384)
    c.close()
