#!/usr/bin/python

# receive file from serve and save as destination

MAXBUFFER = 1048576

import socket
import os
import time

def requestdownload(url,dest):
    s = socket.socket()
    host = socket.gethostname()
    port = 1234
    s.connect(('127.0.0.1',1234))
    
    request = url + '\n' + str(0) + '\n' + str(0)
    
    s.send(request)
    
    fp = open(dest,'ab')
    t = tstart = time.time()
    file = s.recv(16384)
    buffer = ''
    wrote = complete = 0
    speed = 0
    while file:
        buffer += file
        print '%dkB complete. speed = %dkB/s'%(complete,speed)
        complete += 16
        if len(buffer) >= MAXBUFFER:
            fp.write(buffer)
            buffer = ''
            speed = (complete - wrote)/(time.time() - tstart)
            tstart = time.time()
            wrote = complete
        file = s.recv(16384)
    fp.write(buffer)
    fp.close()

if __name__ == '__main__':
    requestdownload('http://mirrors.163.com/debian-cd/6.0.0/i386/iso-cd/debian-6.0.0-i386-businesscard.iso','destination')
