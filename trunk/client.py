#!/usr/bin/python

# receive file from serve and save as destination

MAXBUFFER = 1048576
THREAD = 3
HOST = '127.0.0.1'
HOSTPORT = 1234

import socket
import os,sys
import time
import urllib
import threading


def thread_download(url,start,end,thread_id=0):
    """thread of downloading
    """
    global fp,lock
    
    s = socket.socket()
    try:
        s.connect((HOST,HOSTPORT))
        
        request = url + '\n' + str(start) + '\n' + str(end)
        print request
        
        s.send(request)
        t = tstart = time.time()
        buffer = ''
        wrote = complete = 0
        speed = 0
        while complete <= end-start:
            file = s.recv(16384)
            buffer += file
            complete += len(file)
            if len(buffer) >= MAXBUFFER:
                lock.acquire()
                fp.seek(start+wrote,os.SEEK_SET)
                fp.write(buffer)
                lock.release()
                buffer = ''
                speed = (complete - wrote)/(time.time() - tstart)
                wrote = complete
                print 'thread%d: %dkB complete. speed = %dkB/s'%(thread_id,complete/1024,speed/1024)
                tstart = time.time()
        lock.acquire()
        fp.seek(start+wrote,os.SEEK_SET)
        fp.write(buffer)
        lock.release()
        wrote += len(buffer)
    except socket.timeout:
        print 'time out'
        return wrote

def getUrlFileSize(url, proxies={}):
    urlHandler = urllib.urlopen( url, proxies=proxies )
    headers = urlHandler.info().headers
    length = 0
    for header in headers:
        if header.find('Length') != -1:
            length = header.split(':')[-1].strip()
            length = int(length)
    return length


def requestdownload(url,dest):
    """request a download
    Arguments:
    - `url`: a string of url to download
    - `dest`: destination file name
    """
    global fp,lock
    
    file_size = getUrlFileSize(url)
    try:
        fp = open(dest,'wb')
    except IOError:
        print 'cannot open file!'
        exit()

    thread_download_list = []
    lock = threading.Lock()
    if file_size > THREAD:
        for i in range(THREAD):
            start = file_size/THREAD*i
            end = i!=(THREAD-1) and file_size/THREAD*(i+1)-1 or file_size-1
            thread_download_list.append(threading.Thread(target = thread_download,args=(url,start,end,i)))
            print start,'\n', end
        raw_input()
    else:
        thread_download_list = [threading.Thread(target = thread_download,args=(url,0,0,0))]
    for thread in thread_download_list:
        thread.start()
    for thread in thread_download_list:
        thread.join()
    fp.close()
    print 'download succeeded'

if __name__ == '__main__':
#    socket.setdefaulttimeout(5)
    url = sys.argv[1]
    requestdownload(url,sys.argv[1].split('/')[-1])
