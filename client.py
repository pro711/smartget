#!/usr/bin/python

# receive file from serve and save as destination


THREAD = 1
HOST = '127.0.0.1'
HOSTPORT = 1234
BLOCK_SIZE = 1048576
DATAHUB = ('127.0.0.1',20110)

import socket
import os,sys
import time
import urllib
import threading

def getIdleNode():
    """Get an idle node
    """
    datahub_socket = socket.socket()
    datahub_socket.connect(DATAHUB)
    datahub_socket.send('`requestnodes 1 0')
    datahub_list = datahub_socket.recv(1024).split('\r\n')
    if datahub_list[0] == '200 OK':
        a,p =  datahub_list[1].split(' ')
        datahub_socket.close()
        return (a,int(p))


def downloadBlock(url,start,end,thread_id):
    """thread of downloading a block
    """
    global fp,lock
    
    s = socket.socket()
    try:
        node_addr,node_port = getIdleNode()
        s.connect((node_addr,node_port))
        
        request = url + '\n' + str(start) + '\n' + str(end)
        print request
        
        s.send(request)

        buffer = ''
        complete = 0

        while complete <= end-start:
            file = s.recv(16384)
            buffer += file
            complete += len(file)

        lock.acquire()
        fp.seek(start,os.SEEK_SET)
        print 'writing' + str(len(buffer))
        fp.write(buffer)
        lock.release()
    except socket.timeout:
        print 'time out'
        return
    return 1

def getUrlFileSize(url, proxies={}):
    urlHandler = urllib.urlopen( url, proxies=proxies )
    headers = urlHandler.info().headers
    length = 0
    for header in headers:
        if header.find('Length') != -1:
            length = header.split(':')[-1].strip()
            length = int(length)
    return length

def splitFile(size):
    global block_list
    """Function of split file.
    Every file block is a list of three numbers:
    [start, end, status]
    status: 0:unstarted  1:downloading  2:finished
    """
    block_list = [[BLOCK_SIZE*i,BLOCK_SIZE*(i+1)-1,0] for i in range(size/BLOCK_SIZE)]
    if size % BLOCK_SIZE:
        block_list.append([BLOCK_SIZE*(size/BLOCK_SIZE),size-1,0])
    raw_input('Split file into %d blocks of %dkB.'%(len(block_list),BLOCK_SIZE/1024))

def lookForUnstartedBlock():
    """Look for unstarted block and return it's property list.
    """
    global lock,block_list
    for i in block_list:
        if i[2] == 0:
            return i
    return
    
def thread_download(url,thread_id):
    """Thread of downloading, find undownloaded file blocks and download it.
    
    """
    global lock
    while True:
        lock.acquire()
        block = lookForUnstartedBlock()
        if not block:
            lock.release()
            break
        block[2] = 1
        lock.release()
        if downloadBlock(url,block[0],block[1],thread_id):
            lock.acquire()
            block[2] = 2
            lock.release()
        else:
            lock.acquire()
            block[2] = 0
            lock.release()

def downloadFile(url,dest):
    """request a download
    Arguments:
    - `url`: a string of url to download
    - `dest`: destination file name
    """
    global fp,lock
    global block_list
    
    file_size = getUrlFileSize(url)
    splitFile(file_size)
    try:
        fp = open(dest,'wb')
    except IOError:
        print 'cannot open file!'
        exit()
    time_start = time.time()
    thread_download_list = []
    lock = threading.Lock()
    if file_size > BLOCK_SIZE:
        thread_download_list = [threading.Thread(target = thread_download,args=(url,i)) for i in range(THREAD)]
    else:
        thread_download_list = [threading.Thread(target = thread_download,args=(url,0))]
    for thread in thread_download_list:
        thread.start()
    for thread in thread_download_list:
        thread.join()
    fp.close()
    print 'download succeeded, AVS = %d kB/s'%(file_size/1024/(time.time()-time_start))

if __name__ == '__main__':
#    socket.setdefaulttimeout(5)
    url = sys.argv[1]
    downloadFile(url,sys.argv[1].split('/')[-1])
