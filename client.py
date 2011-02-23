#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       client.py
#       
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>

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
from protocol import SmartGetProtocol
import urlparser

def downloadBlock(url,start,end,thread_id):
    """thread of downloading a block
    """
    global fp,lock,total_completed,file_size,lock_nodes,nodes_linked
    
    s = socket.socket()
    try:
        node = SmartGetProtocol(DATAHUB).requestnodes()
        if not node:
            print 'Get node failed'
            return
        
        lock_nodes.acquire()
        nodes_linked += 1
        lock_nodes.release()
        
        s.connect(node)
        
        request = url + '\n' + str(start) + '\n' + str(end)
        
        s.send(request)

        buffer = ''
        complete = 0

        while complete <= end-start:
            file = s.recv(16384)
            buffer += file
            complete += len(file)

        lock.acquire()
        fp.seek(start,os.SEEK_SET)
        fp.write(buffer)
        total_completed += complete
        lock.release()
        print 'Info: Completed: %d/%dkB'%(total_completed/1024,file_size/1024)
        lock_nodes.acquire()
        print 'Info: LinkedNodes: %d'%nodes_linked
        nodes_linked -= 1
        lock_nodes.release()
        sys.stdout.flush()
        
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
    print 'Split file into %d blocks of %dkB.'%(len(block_list),BLOCK_SIZE/1024)

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
            time.sleep(1)
            lock.release()

def downloadFile(url):
    """request a download
    Arguments:
    - `url`: a string of url to download
    - `dest`: destination file name
    """
    global fp,lock,total_completed,file_size,lock_nodes,nodes_linked
    global block_list

    url,dest = urlparser.UrlParser().parse(url)

    if url.__class__==[].__class__:
        file_size = [getUrlFileSize(i)  for i in url]
        for i in file_size[1:]:
            if file_size[0] != i:
                print "File size doesn't match!"
                exit()
        file_size = file_size[0]
    else:
        file_size = getUrlFileSize(url)

    print 'Info: FileName: '+dest
    print 'Info: BlockSize: '+ str(BLOCK_SIZE)
    print 'Info: FileSize: %dkB'%(file_size/1024)
    sys.stdout.flush()
    
    splitFile(file_size)

    try:
        fp = open(dest,'wb')
    except IOError:
        print 'cannot open file!'
        exit()
    time_start = time.time()
    thread_download_list = []
    nodes_linked = 0
    lock = threading.Lock()
    lock_nodes = threading.Lock()
    total_completed = 0
    
    if file_size > BLOCK_SIZE:
        if url.__class__==[].__class__:
            while len(url)<THREAD:
                url = url * 2
            thread_download_list = [threading.Thread(target = thread_download,args=(url[i],i)) for i in range(THREAD)]
        else:
            thread_download_list = [threading.Thread(target = thread_download,args=(url,i)) for i in range(THREAD)]
    else:
        thread_download_list = [threading.Thread(target = thread_download,args=(url,0))]
    for thread in thread_download_list:
        thread.start()
    for thread in thread_download_list:
        thread.join()
    fp.close()
    print 'Info: Finish: AVS = %d kB/s'%(file_size/1024/(time.time()-time_start))

if __name__ == '__main__':
#    socket.setdefaulttimeout(5)
    url = sys.argv[1]
    downloadFile(url)
