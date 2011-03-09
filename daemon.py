#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       daemon.py
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

# run server, a file named source will be read and sent to client

import socket
import os
from download import MyURLopener
import threading
import time
from protocol import SmartGetProtocol,RegisterError

DOWNLOAD_BLOCK_SIZE = 262144
HOSTNAME = ''
PORT = 1234
DATAHUB = ('127.0.0.1',20110)
THREAD = 2

def thread_send(client,thread_id):
    """
    thread of sending

    """
    global fifo, lock, cv, status
    global finished

    client.setblocking(1)
    while finished[thread_id] == 0:
        lock.acquire()
        try:
            tosend = fifo[thread_id][0]
        except IndexError:
            lock.release()
#            cv.acquire()
            time.sleep(0.1)        # debug
 #           cv.release()
            continue
        lock.release()
        try:
            client.send(tosend)
            del(fifo[thread_id][0])
        except socket.error:
            print 'broken pipe'
            del(fifo[thread_id])
            lock.acquire()
            status += 1
            datahub_protocol_handler.setstatus(status)
            lock.release()
            return
    for i in fifo[thread_id]:
        lock.acquire()
        tosend = i
        lock.release()
        try:
            client.send(tosend)
        except socket.error:
            print 'broken pipe'
            lock.acquire()
            status += 1
            datahub_protocol_handler.setstatus(status)
            lock.release()
            break
    del(fifo[thread_id])
    
def thread_accept(c):
    """
    thread of accepting
    """
    global fifo, lock, cv
    global finished
    global status
    global datahub_protocol_handler

    lock.acquire()
    status -= 1
    lock.release()
    thread_id = threading._get_ident()

    request_list = c.recv(1024).split('\n')
    print 'Got request:\nURL:'+request_list[0]+'\nStart:'+request_list[1]+'\nEnd:'+request_list[2]
    
    opener = MyURLopener()
    try:
        opener.openurl(request_list[0],request_list[1],request_list[2])
    except IOError:
        return
    
    finished[thread_id] = 0

    data = opener.sock.read(16384)
    fifo[thread_id] = []
    thread_send_instance = threading.Thread(target=thread_send,args=(c,thread_id))
    thread_send_instance.start()
    while data:
        if not(thread_send_instance.is_alive()):
            break
        lock.acquire()
        fifo[thread_id].append(data)
        lock.release()
        data = opener.sock.read(DOWNLOAD_BLOCK_SIZE) # debug
    finished[thread_id] = 1
    thread_send_instance.join()
    c.close()
    lock.acquire()
    status += 1
    datahub_protocol_handler.setstatus(status)
    lock.release()

def main():
    global fifo, lock, cv
    global finished, status
    global datahub_protocol_handler
    lock = threading.Lock()
    status = THREAD
    fifo = {}
    finished = {}
    thread_accept_list = []

    datahub_protocol_handler = SmartGetProtocol(DATAHUB,PORT)

    try:
        datahub_protocol_handler.register()
    except RegisterError:
        datahub_protocol_handler.deregister()
        datahub_protocol_handler.register()

    datahub_protocol_handler.setstatus(status)
        
    s = socket.socket()
    s.bind((HOSTNAME,PORT))
    s.settimeout(None)
    s.listen(5)
    cv = threading.Condition()
    
    try:
        while True:
            c,addr=s.accept()
            print 'Got connection from',addr
            thread_accept_instance = threading.Thread(target=thread_accept,args=((c,)))
            thread_accept_list.append(thread_accept_instance)
            thread_accept_instance.start()
    except KeyboardInterrupt:
        print '\nInterrupted by user.\nExiting...'
        datahub_protocol_handler.deregister()
        exit()
        
        

if __name__ == '__main__':
    socket.setdefaulttimeout(5)
    main()
