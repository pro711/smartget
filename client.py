#!/usr/bin/python

# receive file from serve and save as destination
n
MAXBUFFER = 1048576

import socket
import os,sys
import time

def requestdownload(url,dest):
    s = socket.socket()
    host = socket.gethostname()
    port = 1234
    try:
        s.connect(('127.0.0.1',1234))
        
        request = url + '\n' + str(0) + '\n' + str(0)
        
        s.send(request)
        try:
            fp = open(dest,'ab')
        except IOError:
            print 'Open file Error.'
            exit()
        t = tstart = time.time()
        file = s.recv(16384)
        buffer = ''
        wrote = complete = 0
        speed = 0
        while file:
            buffer += file
            print '%dkB complete. speed = %dkB/s'%(complete,speed)
            complete += len(file)/1024
            if len(buffer) >= MAXBUFFER:
                fp.write(buffer)
                buffer = ''
                speed = (complete - wrote)/(time.time() - tstart)
                tstart = time.time()
                wrote = complete
            file = s.recv(16384)
        fp.write(buffer)
        fp.close()
    except socket.timeout:
        print 'time out'
        exit()

if __name__ == '__main__':
    socket.setdefaulttimeout(5)
    url = sys.argv[1]
    requestdownload(url,sys.argv[1].split('/')[-1])
